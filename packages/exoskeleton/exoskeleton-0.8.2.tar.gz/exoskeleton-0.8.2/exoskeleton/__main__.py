#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exoskeleton Crawler Framework
~~~~~~~~~~~~~~~~~~~~~
A Python framework to build a basic crawler / scraper with a MariaDB backend.
"""

# python standard library:
from collections import Counter
import errno
import logging
import os
import queue
import random
import time
from typing import Union
from urllib.parse import urlparse


# 3rd party libraries:
import pymysql
import requests

# import other modules of this framework
import exoskeleton.checks as checks
import exoskeleton.communication as communication
import exoskeleton.utils as utils



class Exoskeleton:
    u""" Main class of the exoskeleton crawler framework. """
    # The class is complex which leads pylint3 to complain a lot.
    # As the complexity is needed, disable some warnings:
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-public-methods
    # pylint: disable=too-many-branches

    def __init__(self,
                 database_name: str,
                 database_user: str,
                 database_passphrase: str,
                 database_host: str = 'localhost',
                 database_port: int = None,
                 project_name: str = 'Bot',
                 bot_user_agent: str = 'BOT (http://www.example.com)',
                 min_wait: float = 5.0,
                 max_wait: float = 20.0,
                 mail_server: str = 'localhost',
                 mail_admin: str = None,
                 mail_sender: str = None,
                 milestone_num: int = None,
                 target_directory: str = None,
                 queue_stop_on_empty: bool = False,
                 filename_prefix: str = ''):
        u"""Sets defaults"""

        logging.info('You are using exoskeleton 0.8.2 (beta / Feb 21, 2020)')

        self.PROJECT = project_name.strip()
        self.USER_AGENT = bot_user_agent.strip()

        self.DB_HOSTNAME = database_host.strip()

        self.DB_PORT = checks.validate_port(database_port)
        self.DB_NAME = database_name.strip()
        self.DB_USERNAME = database_user.strip()
        self.DB_PASSPHRASE = database_passphrase.strip()
        if self.DB_PASSPHRASE == '':
            logging.warning('No database passphrase provided.')

        self.connection = None
        self.establish_db_connection()
        self.cur = self.connection.cursor()
        self.check_table_existence()
        self.check_stored_procedures()

        self.CONNECTION_TIMEOUT = self.get_connection_timeout()

        self.HASH_METHOD = checks.check_hash_algo(self.get_setting('FILE_HASH_METHOD'))

        self.MAIL_START_MSG = True if self.get_setting('MAIL_START_MSG') == 'True' else False
        self.MAIL_FINISH_MSG = True if self.get_setting('MAIL_FINISH_MSG') == 'True' else False
        self.MILESTONE = None
        if isinstance(milestone_num, int):
            self.MILESTONE = milestone_num
        elif milestone_num is not None:
            raise ValueError

        self.MAIL_ADMIN = None
        if checks.check_email_format(mail_admin):
            self.MAIL_ADMIN = mail_admin.strip()
        self.MAIL_SENDER = None
        if checks.check_email_format(mail_sender):
            self.MAIL_SENDER = mail_sender.strip()

        self.MAIL_SEND = False
        if self.MAIL_ADMIN and self.MAIL_SENDER:
            # needing both to send mails
            self.MAIL_SEND = True
        elif self.MILESTONE:
            logging.error('Cannot send mail when milestone is reached. ' +
                          'Either sender or receiver for mails is missing.')
        elif self.MAIL_FINISH_MSG:
            logging.error('Cannot send mail when bot is done. ' +
                          'Either sender or receiver for mails is missing.')

        self.QUEUE_MAX_RETRY = 3 # NOT YET IMPLEMENTET
        if self.get_numeric_setting('QUEUE_MAX_RETRY') is not None:
            self.QUEUE_MAX_RETRY = int(self.get_numeric_setting('QUEUE_MAX_RETRY'))
        self.QUEUE_REVISIT = 60.0
        if self.get_numeric_setting('QUEUE_REVISIT') is not None:
            self.QUEUE_REVISIT = self.get_numeric_setting('QUEUE_REVISIT')

        self.WAIT_MIN = 5.0
        if type(min_wait) in (int, float):
            self.WAIT_MIN = min_wait
        self.WAIT_MAX = 20.0
        if type(max_wait) in (int, float):
            self.WAIT_MAX = max_wait

        self.cnt = Counter() # type: Counter

        self.TARGET_DIR = os.getcwd()

        if target_directory is None or target_directory == '':
            logging.warning("Target directory is not set. " +
                            "Using the current working directory " +
                            "%s to store files!",
                            self.TARGET_DIR)
        else:
            # Assuming that if a directory was set, it has
            # to be used. Therefore no fallback to the current
            # working directory.
            target_directory = target_directory.strip()
            if os.path.isdir(target_directory):
                self.TARGET_DIR = target_directory
                logging.debug("Set target directory to %s",
                              target_directory)
            else:
                raise OSError("Cannot find or access the user " +
                              "supplied target directory! " +
                              "Create this directory or check permissions.")


        self.QUEUE_STOP_IF_EMPTY = queue_stop_on_empty

        self.FILE_PREFIX = filename_prefix.strip()

        self.BOT_START = time.monotonic()
        self.PROCESS_TIME_START = time.process_time()
        logging.debug('started timer')

        self.local_download_queue = queue.Queue() # type: queue.Queue

        self.MAX_PATH_LENGTH = 255

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SETTINGS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def get_setting(self,
                    key: str) -> Union[str, None]:
        u""" Get setting from the database table by using the key. """
        self.cur.execute('SELECT settingValue ' +
                         'FROM settings ' +
                         'WHERE settingKey = %s;', key)
        try:
            return self.cur.fetchone()[0] # type: ignore
        except TypeError:
            logging.error('Setting not available')
            return None

    def get_numeric_setting(self,
                            key: str) -> Union[float, None]:
        u""" Get numeric setting. Raise ValueError if field's content
        cannot be coerced into float. """
        try:
            setting_value = float(self.get_setting(key))
            if setting_value is not None:
                return setting_value
            else:
                raise ValueError
        except ValueError:
            logging.error('Setting field %s contains non-numeric value.', key)
            return None

    def get_connection_timeout(self) -> Union[float, int]:
        u""" Connection timeout is set in the settings table. """

        timeout = self.get_numeric_setting('CONNECTION_TIMEOUT')

        if timeout is None:
            logging.error('Setting CONNECTION_TIMEOUT is missing. '+
                          'Fallback to 60 seconds.')
            return 60

        try:
            if timeout <= 0:
                logging.error('Negative or zero value for timeout. ' +
                              'Fallback to 60 seconds.')
                return 60
            else:
                if timeout > 120:
                    logging.info('Very high value for timeout: ' +
                                 '%s seconds', timeout)
            logging.debug('Connection timeout set to %s s.', timeout)
            return timeout
        except TypeError:
            logging.error('Invalid format for setting CONNECTION_TIMEOUT. ' +
                          'Fallback to 60 seconds.')
            return 60


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ACTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def __get_object(self,
                     queue_id: int,
                     action_type: str,
                     url: str,
                     url_hash: str):
        u""" Generic function to either download a file or store a page's content. """
        # pylint: disable=too-many-branches
        if not isinstance(queue_id, int):
            raise ValueError('The queue_id must be an integer.')
        if action_type not in ('file', 'content'):
            raise ValueError('Invalid action')
        if url == '' or url is None:
            raise ValueError('Missing url')
        url = url.strip()
        if url_hash == '' or url_hash is None:
            raise ValueError('Missing url_hash')

        try:
            if action_type == 'file':
                name, ext = os.path.splitext(url)
                new_filename = f"{self.FILE_PREFIX}{queue_id}{ext}"

                # TO Do: more generic pathhandling
                target_path = self.TARGET_DIR + '/' + new_filename

                logging.debug('starting download of queue id %s', queue_id)
                r = requests.get(url,
                                 headers={"User-agent": str(self.USER_AGENT)},
                                 timeout=self.CONNECTION_TIMEOUT,
                                 stream=True)
            elif action_type == 'content':
                logging.debug('retrieving content of queue id %s', queue_id)
                r = requests.get(url,
                                 headers={"User-agent": str(self.USER_AGENT)},
                                 timeout=self.CONNECTION_TIMEOUT,
                                 stream=False
                                )

            if r.status_code == 200:
                mime_type = ''
                if r.headers.get('content-type') is not None:
                    mime_type = (r.headers.get('content-type')).split(';')[0] # type: ignore

                if action_type == 'file':
                    with open(target_path, 'wb') as file_handle:
                        for block in r.iter_content(1024):
                            file_handle.write(block)
                        logging.debug('file written')
                        hash_value = None
                        if self.HASH_METHOD:
                            hash_value = utils.get_file_hash(target_path,
                                                             self.HASH_METHOD)

                    logging.debug('file written to disk')
                    try:
                        self.cur.callproc('insert_file_SP',
                                          (url, url_hash, queue_id, mime_type,
                                           self.TARGET_DIR, new_filename,
                                           utils.get_file_size(target_path),
                                           self.HASH_METHOD, hash_value))
                    except pymysql.DatabaseError:
                        self.cnt['transaction_fail'] += 1
                        logging.error('Transaction failed: Could not add already ' +
                                      'downloaded file %s to the database!',
                                      new_filename)

                elif action_type == 'content':

                    detected_encoding = str(r.encoding)
                    logging.debug('detected encoding: %s', detected_encoding)
                    try:
                        # Stored procedure saves the content,
                        # transfers the labels from the queue,
                        # and removes the queue item:
                        self.cur.callproc('insert_content_SP',
                                          (url, url_hash, queue_id,
                                           mime_type, r.text))
                    except pymysql.DatabaseError:
                        self.cnt['transaction_fail'] += 1
                        logging.error('Transaction failed: Could not add page code ' +
                                      'of queue item %s to the database!', queue_id)

                self.cnt['processed'] += 1
                self.__update_host_statistics(url, True)

            if r.status_code in (402, 403, 404, 405, 410, 451):
                self.mark_error(queue_id, r.status_code)
                self.__update_host_statistics(url, False)
            elif r.status_code == 429:
                logging.error('The bot hit a rate limit! It queries too ' +
                              'fast => increase min_wait.')
                self.add_crawl_delay_to_item(queue_id)
                self.__update_host_statistics(url, False)
            elif r.status_code not in (200, 402, 403, 404, 405, 410, 429, 451):
                logging.error('Unhandeled return code %s', r.status_code)
                self.__update_host_statistics(url, False)

        except TimeoutError:
            logging.error('Reached timeout.',
                          exc_info=True)
            self.add_crawl_delay_to_item(queue_id)
            self.__update_host_statistics(url, False)

        except ConnectionError:
            logging.error('Connection Error', exc_info=True)
            self.__update_host_statistics(url, False)
            raise

        except requests.exceptions.MissingSchema:
            logging.error('Missing Schema Exception. Does your URL contain the ' +
                          'protocol i.e. http:// or https:// ? See queue_id = %s',
                          queue_id)
            self.mark_error(queue_id, 1)

        except Exception:
            logging.error('Unknown exception while trying ' +
                          'to download.', exc_info=True)
            self.__update_host_statistics(url, False)
            raise

    def get_file(self,
                 queue_id: int,
                 url: str,
                 url_hash: str):
        u"""Download a file and save it in the specified folder."""
        self.__get_object(queue_id, 'file', url, url_hash)

    def store_page_content(self,
                           url: str,
                           url_hash: str,
                           queue_id: int):
        u"""Retrieve a page and store it's content to the database. """
        self.__get_object(queue_id, 'content', url, url_hash)

    def return_page_code(self,
                         url: str):
        u"""Directly return a page's code and do *not* store it
        in the database. """
        if url == '' or url is None:
            raise ValueError('Missing url')
        url = url.strip()

        try:
            r = requests.get(url,
                             headers={"User-agent": str(self.USER_AGENT)},
                             timeout=self.CONNECTION_TIMEOUT,
                             stream=False
                            )

            if r.status_code == 200:
                return r.text
            else:
                raise RuntimeError('Cannot return page code')

        except TimeoutError:
            logging.error('Reached timeout.', exc_info=True)
            self.__update_host_statistics(url, False)
            raise

        except ConnectionError:
            logging.error('Connection Error', exc_info=True)
            self.__update_host_statistics(url, False)
            raise

        except Exception:
            logging.exception('Unknown exception while trying to get page-code', exc_info=True)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATABASE MANAGEMENT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def establish_db_connection(self):
        u"""Establish a connection to MariaDB """

        if not (self.DB_HOSTNAME and
                self.DB_PORT and
                self.DB_NAME and
                self.DB_USERNAME):

            # give specific error messages:
            missing_params = []
            if not self.DB_HOSTNAME:
                missing_params.append('hostname')
            if not self.DB_PORT:
                missing_params.append('port')
            if not self.DB_NAME:
                missing_params.append('database name')
            if not self.DB_USERNAME:
                missing_params.append('username')
            # ... stop before connection try:
            raise ValueError('The following parameters were not supplied, ' +
                             'but are needed to connect to the database: ' +
                             '{}'.format(','.join(missing_params)))

        try:
            logging.debug('Trying to connect to database.')
            self.connection = pymysql.connect(host=self.DB_HOSTNAME,
                                              port=self.DB_PORT,
                                              database=self.DB_NAME,
                                              user=self.DB_USERNAME,
                                              password=self.DB_PASSPHRASE,
                                              autocommit=True)

            logging.info('Established database connection.')

        except pymysql.InterfaceError:
            logging.exception('Exception related to the database ' +
                              '*interface*.', exc_info=True)
            raise
        except pymysql.DatabaseError:
            logging.exception('Exception related to the database.',
                              exc_info=True)
            raise
        except Exception:
            logging.exception('Unknown exception while ' +
                              'trying to connect to the DBMS.',
                              exc_info=True)
            raise

    def check_table_existence(self) -> bool:
        u"""Check if all expected tables exist."""
        logging.debug('Checking if the database table structure is complete.')
        expected_tables = ['actions', 'errorType', 'eventLog',
                           'fileContent', 'fileMaster', 'fileVersions',
                           'labels', 'labelToMaster', 'labelToQueue', 'labelToVersion',
                           'queue', 'settings', 'statisticsHosts', 'storageTypes']
        tables_count = 0

        self.cur.execute('SHOW TABLES;')
        tables = self.cur.fetchall()
        if not tables:
            logging.error('The database exists, but no tables found!')
            raise OSError('Database table structure missing. Run generator script!')
        else:
            tables_found = [item[0] for item in tables]
            for table in expected_tables:
                if table in tables_found:
                    tables_count += 1
                    logging.debug('Found table %s', table)
                else:
                    logging.error('Table %s not found.', table)

        if tables_count != len(expected_tables):
            raise RuntimeError('Database Schema Incomplete: Missing Tables!')

        logging.info("Found all expected tables.")
        return True

    def check_stored_procedures(self) -> bool:
        u"""Check if all expected stored procedures exist and if the user
        is allowed to execute them. """
        logging.debug('Checking if stored procedures exist.')
        expected_procedures = ['delete_all_versions_SP',
                               'delete_from_queue_SP',
                               'insert_content_SP',
                               'insert_file_SP',
                               'transfer_labels_from_queue_to_master_SP']

        procedures_count = 0
        self.cur.execute('SELECT SPECIFIC_NAME FROM INFORMATION_SCHEMA.ROUTINES ' +
                         'WHERE ROUTINE_SCHEMA = %s;',
                         self.DB_NAME)
        procedures = self.cur.fetchall()
        procedures_found = [item[0] for item in procedures]
        for procedure in expected_procedures:
            if procedure in procedures_found:
                procedures_count += 1
                logging.debug('Found stored procedure %s', procedure)
            else:
                logging.error('Stored Procedure %s is missing (create it ' +
                              'with the database script) or the user lacks ' +
                              'permissions to use it.', procedure)

        if procedures_count != len(expected_procedures):
            raise RuntimeError('Database Schema Incomplete: Missing Stored Procedures!')

        logging.info("Found all expected stored procedures.")
        return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# JOB MANAGEMENT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def job_define_new(self,
                       job_name: str,
                       start_url: str):
        u""" Create a new crawl job identified by it name and an url
        to start crawling. """
        if job_name == '' or job_name is None:
            raise ValueError
        job_name = job_name.strip()
        if len(job_name) > 127:
            raise ValueError('Invalid job name: maximum 127 characters.')

        if start_url == '' or start_url is None:
            raise ValueError

        try:
            self.cur.execute('INSERT INTO jobs ' +
                             '(jobName, startUrl, startUrlHash) ' +
                             'VALUES (%s, %s, SHA2(%s,256));',
                             (job_name, start_url, start_url))
            logging.debug('Defined new job.')
        except pymysql.IntegrityError:
            # A job with this name already exists
            # Check if startURL is the same:
            self.cur.execute('SELECT startURL FROM jobs WHERE jobName = %s;',
                             job_name)
            existing_start_url = self.cur.fetchone()[0]
            if existing_start_url == start_url:
                logging.warning('A job with identical name and startURL is already defined.')
            else:
                raise ValueError('A job with the identical name but ' +
                                 '*different* startURL is already defined!')

    def job_update_current_url(self,
                               job_name: str,
                               current_url: str):
        u""" Set the currentUrl for a specific job. """

        if job_name == '' or job_name is None:
            raise ValueError('Provide the job name.')
        if current_url == '' or current_url is None:
            raise ValueError('Current URL must not be empty.')

        affected_rows = self.cur.execute('UPDATE jobs ' +
                                         'SET currentURL = %s ' +
                                         'WHERE jobName = %s;',
                                         (current_url, job_name))
        if affected_rows == 0:
            raise ValueError('A job with this name is not known.')


    def job_get_current_url(self,
                            job_name: str) -> str:
        u""" Returns the current URl for this job. If none is stored, this
        returns the start URL. Raises exception if the job is already finished. """

        self.cur.execute('SELECT finished FROM jobs ' +
                         'WHERE jobName = %s;',
                         job_name)
        job_state = self.cur.fetchone()
        # If the job does not exist at all, then MariaDB returns None.
        # If the job exists, but the finished field has a value of NULL,
        # then MariaDB returns (None,)
        try:
            job_state = job_state[0]
        except TypeError:
            # Occurs if the the result was None, i.e. the job
            # does not exist.
            raise ValueError('Job is unknown!')

        if job_state is not None:
            # i.e. the finished field is not empty
            raise RuntimeError(f"Job already finished at {job_state}.")

        # The job exists and is not finished. So return the currentUrl,
        # or - in case that is not defined - the startUrl value.
        self.cur.execute('SELECT COALESCE(currentUrl, startUrl) ' +
                         'FROM jobs ' +
                         'WHERE jobName = %s;',
                         job_name)
        return self.cur.fetchone()[0]

    def job_mark_as_finished(self,
                             job_name: str):
        u""" Mark a crawl job as finished. """
        if job_name == '' or job_name is None:
            raise ValueError
        job_name = job_name.strip()
        affected_rows = self.cur.execute('UPDATE jobs SET ' +
                                         'finished = CURRENT_TIMESTAMP() ' +
                                         'WHERE jobName = %s;',
                                         job_name)
        if affected_rows == 0:
            raise ValueError('A job with this name is not known.')
        logging.debug('Marked job %s as finished.', job_name)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# QUEUE MANAGEMENT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def random_wait(self):
        u"""Waits for a random time between actions
        (within the interval preset at initialization).
        This is done to avoid to accidentially overload
        the queried host. Some host actually enforce
        limits through IP blocking."""
        query_delay = random.randint(self.WAIT_MIN, self.WAIT_MAX) # nosec
        logging.debug("%s seconds delay until next action", query_delay)
        time.sleep(query_delay)
        return

    def num_items_in_queue(self) -> int:
        u"""Number of items left in the queue. """
        # How many are left in the queue?
        self.cur.execute("SELECT COUNT(*) FROM queue " +
                         "WHERE causesError IS NULL;")
        return int(self.cur.fetchone()[0]) # type: ignore

    def absolute_run_time(self) -> float:
        u"""Return seconds since init. """
        return time.monotonic() - self.BOT_START

    def get_process_time(self) -> float:
        u"""Return execution time since init"""
        return time.process_time() - self.PROCESS_TIME_START

    def estimate_remaining_time(self) -> float:
        u"""estimate remaining seconds to finish crawl."""
        time_so_far = self.absolute_run_time()
        num_remaining = self.num_items_in_queue()

        if self.cnt['processed'] > 0:
            time_each = time_so_far / self.cnt['processed']
            return num_remaining * time_each

        logging.warning('Cannot estimate remaining time ' +
                        'as there are no data so far.')
        return -1

    def add_file_download(self,
                          url: str,
                          labels: set = None):
        u"""add a file download URL to the queue """
        self.add_to_queue(url, 1, labels)

    def add_save_page_code(self,
                           url: str,
                           labels: set = None):
        u""" add an URL to the queue to save it's HTML code into the database."""
        self.add_to_queue(url, 2, labels)

    def add_to_queue(self,
                     url: str,
                     action: int,
                     labels: set = None):
        u""" More general function to add items to queue. Called by
        add_file_download and add_save_page_code."""

        if action not in (1, 2):
            logging.error('Invalid value for action to take!')
            return

        # Excess whitespace might be common (copy and paste)
        # and would change the hash:
        url = url.strip()

        # check if the file already has been processed
        self.cur.execute('SElECT id FROM fileMaster ' +
                         'WHERE urlHash = SHA2(%s,256);', url)
        id_in_file_master = self.cur.fetchone()
        if id_in_file_master is not None:
            logging.info('The file has already been processed. Skipping it.')
            # Add possibly new labels to fileMaster
            self.assign_labels(id_in_file_master, labels, 'master')
            return

        try:
            # add the new element to the queue
            self.cur.execute('INSERT INTO queue (action, url, urlHash) ' +
                             'VALUES (%s, %s, SHA2(%s,256));',
                             (action, url, url))

            # get the id in the queue
            self.cur.execute('SELECT id FROM queue ' +
                             'WHERE urlHash = SHA2(%s,256) ' +
                             'LIMIT 1;', url)
            queue_id = self.cur.fetchone()[0] # type: ignore

            # link labels to queue item
            if labels:
                self.assign_labels(queue_id, labels, 'queue')

        except pymysql.IntegrityError:
            # No further check here as an duplicate url / urlHash is
            # the only thing that can cause that error here.
            logging.info('URL already in queue. Not adding it again.')

            # get the id in the queue
            self.cur.execute('SELECT id FROM queue ' +
                             'WHERE urlHash = SHA2(%s,256) ' +
                             'LIMIT 1;', url)
            queue_id = self.cur.fetchone()[0] # type: ignore
            # add possibly new labels
            self.assign_labels(queue_id, labels, 'queue')

    def delete_from_queue(self,
                          queue_id: int):
        u"""Remove all label links from a queue item and then delete it from the queue."""
        # callproc expects a tuple. Do not remove the comma.
        self.cur.callproc('delete_from_queue_SP', (queue_id, ))

    def add_crawl_delay_to_item(self,
                                queue_id: int,
                                delay_seconds: int = None):
        u"""In case of timeout or temporary error add a delay until
        the same URL is queried again. """
        logging.debug('Adding crawl delay to queue item %s', queue_id)
        waittime = 30
        if delay_seconds:
            waittime = delay_seconds

        self.cur.execute('UPDATE queue ' +
                         'SET delayUntil = ADDTIME(NOW(), %s) ' +
                         'WHERE id = %s', (waittime, queue_id))

    def mark_error(self,
                   queue_id: int,
                   error: int):
        u""" Mark item in queue that causes permant error.

        Has to be marked as otherwise exoskelton will try to
        download it over and over again."""

        self.cur.execute('UPDATE queue ' +
                         'SET causesError = %s ' +
                         'WHERE id = %s;', (error, queue_id))
        logging.debug('Marked queue-item that caused a problem.')
        if error in (429, 500, 503):
            self.add_crawl_delay_to_item(queue_id, 600)

    def process_queue(self):
        u"""Process the queue"""
        while True:
            # get the next suitable task
            self.cur.execute('SELECT ' +
                             '  id' +
                             '  ,action' +
                             '  ,url ' +
                             '  ,urlHash ' +
                             'FROM queue ' +
                             'WHERE causesError IS NULL AND ' +
                             '(delayUntil IS NULL OR delayUntil < NOW()) ' +
                             'ORDER BY addedToQueue ASC ' +
                             'LIMIT 1;')
            next_in_queue = self.cur.fetchone()
            if next_in_queue is None:
                # empty queue: either full stop or wait for new tasks
                if self.QUEUE_STOP_IF_EMPTY:
                    logging.info('Queue empty. Bot stops as configured to do.')
                    subject = f"{self.PROJECT}: queue empty / bot stopped"
                    content = (f"The queue is empty. The bot {self.PROJECT} " +
                               f"stopped as configured.")
                    if self.MAIL_SEND:
                        communication.send_mail(self.MAIL_ADMIN,
                                                self.MAIL_SENDER,
                                                subject, content)
                    break
                else:
                    logging.debug("Queue empty. Waiting %s seconds until next check",
                                  self.QUEUE_REVISIT)
                    time.sleep(self.QUEUE_REVISIT)
                    continue
            else:
                # got a task from the queue
                queue_id = next_in_queue[0]
                action = next_in_queue[1]
                url = next_in_queue[2]
                url_hash = next_in_queue[3]

                if action == 1:
                    # download file to disk
                    self.get_file(queue_id, url, url_hash)
                elif action == 2:
                    # save page code into database
                    self.store_page_content(url, url_hash, queue_id)
                else:
                    logging.error('Unknown action id!')

                if self.MILESTONE:
                    self.check_milestone()

                # wait some interval to avoid overloading the server
                self.random_wait()

    def __update_host_statistics(self,
                                 url: str,
                                 success: bool = True):
        u""" Updates the host based statistics"""

        fqdn = urlparse(url).hostname
        if success:
            successful, problems = 1, 0
        else:
            successful, problems = 0, 1

        self.cur.execute('INSERT INTO statisticsHosts ' +
                         '(fqdnHash, fqdn, successful, ' +
                         'problems) ' +
                         'VALUES (MD5(%s), %s, %s, %s) ' +
                         'ON DUPLICATE KEY UPDATE ' +
                         'successful = successful + %s, ' +
                         'problems = problems + %s;',
                         (fqdn, fqdn, successful, problems,
                          successful, problems))

    def check_milestone(self):
        u""" Check if milestone is reached. In case,
        send mail (if configured so)."""
        processed = self.cnt['processed']
        if isinstance(self.MILESTONE, int):
            if processed % self.MILESTONE == 0:
                logging.info("Milestone reached: %s processed",
                             str(processed))

            if self.MAIL_SEND:
                subject = (f"{self.PROJECT} Milestone reached: " +
                           f"{self.cnt['processed']} processed")
                content = (f"{self.cnt['processed']} processed.\n" +
                           f"{self.num_items_in_queue()} items " +
                           f"remaining in the queue.\n" +
                           f"Estimated time to complete queue: " +
                           f"{self.estimate_remaining_time()} seconds.\n")
                communication.send_mail(self.MAIL_ADMIN,
                                        self.MAIL_SENDER,
                                        subject, content)

            return True

        elif isinstance(self.MILESTONE, list):
            logging.error("Feature not yet implemented")
            return False
        else:
            raise TypeError('Milestone has either be int or list')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LABELS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def define_new_label(self,
                         shortname: str,
                         description: str = None):
        u""" If the label is not already in use, define a new label
        and a description. """
        if len(shortname) > 31:
            logging.error("Labelname exceeds max length of 31 " +
                          "characters. Cannot add it.")
            return
        try:
            self.cur.execute('INSERT INTO labels (shortName, description) ' +
                             'VALUES (%s, %s);',
                             (shortname, description))

            logging.debug('Added label to the database.')
        except pymysql.err.IntegrityError:
            logging.debug('Label already existed.')

    def define_or_update_label(self,
                               shortname: str,
                               description: str = None):
        u""" Insert a new label into the database or update it's
        description in case it already exists. Use define_new_label
        if an update has to be avoided. """
        if len(shortname) > 31:
            logging.error("Labelname exceeds max length of 31 " +
                          "characters. Cannot add it.")
            return

        self.cur.execute('INSERT INTO labels (shortName, description) ' +
                         'VALUES (%s, %s) ' +
                         'ON DUPLICATE KEY UPDATE description = %s;',
                         (shortname, description, description))

    def get_label_ids(self,
                      label_set: set):
        u""" Given a set of labels, this returns the corresponding ids
        in the labels table. """
        if label_set:
            # The IN-Operator makes it necessary to construct the command
            # every time, so input gets escaped. See the accepted answer here:
            # https://stackoverflow.com/questions/14245396/using-a-where-in-statement
            query = ("SELECT id " +
                     "FROM labels " +
                     "WHERE shortName " +
                     "IN ({0});".format(', '.join(['%s'] * len(label_set))))
            self.cur.execute(query, tuple(label_set))
            label_id = self.cur.fetchall()

            return None if label_id is None else label_id
        logging.error('No labels provided to get_label_ids().')
        return None

    def assign_labels(self,
                      object_id: int,
                      labels: set,
                      target: str):
        u""" Assigns one or multiple labels either to an item
        in the master, the queue or a version.
        Removes duplicates and adds new labels to the label list
        if necessary.."""

        # Using a set to avoid duplicates. However, accept either
        # a single string or a list type.

        if labels:
            label_set = utils.convert_to_set(labels)

            for label in label_set:
                # Make sure all labels are in the database table.
                # -> If they already exist or malformed the command
                # will be ignored by the dbms.
                self.define_new_label(label)

            # Get all label-ids
            id_list = self.get_label_ids(label_set)

            # Check if there are already labels assigned
            if target == 'queue':
                self.cur.execute('SELECT labelID FROM labelToQueue ' +
                                 'WHERE queueID = %s;', object_id)
                ids_associated = self.cur.fetchall()

                # ignore all labels already associated
                id_list = tuple(set(id_list) - set(ids_associated))
            elif target == 'master':
                self.cur.execute('SELECT labelID FROM labelToMaster ' +
                                 'WHERE labelID = %s;', object_id)
                ids_associated = self.cur.fetchall()

                # ignore all labels already associated
                id_list = tuple(set(id_list) - set(ids_associated))

            if id_list:
                # Case: there are new labels
                # Convert into a format to INSERT with executemany
                insert_list = [(id[0], object_id) for id in id_list]
            else:
                logging.debug('No labels to add.')
                return

            if target == 'queue':
                self.cur.executemany('INSERT IGNORE INTO labelToQueue ' +
                                     '(labelID, queueID) ' +
                                     'VALUES (%s, %s);', insert_list)

            elif target == 'master':
                self.cur.executemany('INSERT IGNORE INTO labelToMaster ' +
                                     '(labelID, masterID) ' +
                                     'VALUES (%s, %s);', insert_list)

            elif  target == 'version':
                self.cur.executemany('INSERT IGNORE INTO labelToVersion ' +
                                     '(labelID, versionID) ' +
                                     'VALUES (%s, %s);', insert_list)

            else:
                raise ValueError('The target parameter has to be ' +
                                 'either master, queue, or version.')

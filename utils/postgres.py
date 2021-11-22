__author__ = "sarvesh.singh"

import psycopg2
import os
from psycopg2.extras import RealDictCursor
from utils.logger import Logger


class Postgres:
    """
    DB Connector
    """

    def __init__(self, host, username, password, database=None, port=None):
        """
        Connect to database and provide it's marker
        :param host:
        :param username:
        :param password:
        :param database:
        :param port:
        """
        self.host = host
        self.port = port
        self.logger = Logger(name="DB").get_logger
        if self.port is None:
            self.port = 5432
        self.username = username
        self.password = password
        self.database = database

        # variables
        self.connection = None
        self._connect_to_db()

    def _connect_to_db(self):
        """
        Function to connect to db
        :return:
        """
        self.logger.debug(
            f"Making Connection to DB with {self.username} {self.password} {self.host} {self.port} {self.database}"
        )
        self.connection = psycopg2.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            connect_timeout=120,
            options="-c statement_timeout=120s",
        )
        self.connection.set_session(autocommit=True)

    def execute_sql_script(self, script_name):
        """
        Execute an SQL Script on Database
        :param script_name:
        :return:
        """

        self.logger.debug(f"Running SQL Script {script_name}")
        if not os.path.isfile(script_name):
            raise Exception(f"File {script_name} does not exist !!")

        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(open(script_name, "r").read())
            if cur.rowcount >= 0:
                return cur.fetchall()
            return None

    def run_query(self, query):
        """
        Run db Query Only
        :param query:
        :return:
        """

        self.logger.debug(f"Running SQL Query {query} but not fetching data ...")
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.rowcount

    def run_and_fetch_data(self, query):
        """
        Run db Query and Fetch Data from Database
        :param query:
        :return:
        """
        self.logger.debug(f"Running SQL Query {query} and fetching data ...")
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            records = cur.fetchall()
            return records

    def delete_data_query(self, table, condition):
        """
        Function to run query to delete data from database
        :param table:
        :param condition:
        :return:
        """
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            _query = f"DELETE FROM {table} {condition}"
            cur.execute(_query)
            return cur.rowcount

    def insert_columns(self, query):
        """
        Function to insert new columns in db
        :param query:
        :return:
        """
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.rowcount

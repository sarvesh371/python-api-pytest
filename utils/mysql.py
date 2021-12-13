__author__ = 'sarvesh.singh'

from utils.logger import Logger
import mysql.connector

logger = Logger(name='MYSQL').get_logger


class MySql:
    """
    MySql Connector for Devx
    """

    def __init__(self, host, username, password, database=None):
        """
        Connect to database and provide it's marker
        :param host:
        :param username:
        :param password:
        :param database:
        """
        logger.debug('Connecting to mysql !!')
        self._host = host
        self._username = username
        self._password = password
        self._database = database

        # variables
        self._connection = None
        self._connection_cursor = None
        self._connect_to_db()

    def _connect_to_db(self):
        """
        Function to connect to db
        :return:
        """
        logger.debug(
            f'Making Connection to DB with {self._username} {self._password} {self._host} {self._database}'
        )
        self._connection = mysql.connector.connect(
            host=self._host,
            user=self._username,
            password=self._password,
            database=self._database
        )
        self._connection_cursor = self._connection.cursor()

    def run_query(self, query):
        """
        Run db Query Only
        :param query:
        :return:
        """
        logger.debug(f'Running SQL Query {query} but not fetching data ...')
        self._connection_cursor.execute(query)

    def run_and_fetch_data(self, query):
        """
        Run db Query and Fetch Data from Database
        :param query:
        :return:
        """
        logger.debug(f'Running SQL Query {query} and fetching data ...')
        self._connection_cursor.execute(query)
        return self._connection_cursor.fetchall()

    def delete_data_query(self, table, condition):
        """
        Function to run query to delete data from database
        :param table:
        :param condition:
        :return:
        """
        sql = f'DELETE FROM {table} WHERE {condition}'
        logger.debug(f'Running Delete Query {sql}')
        self._connection_cursor.execute(sql)
        self._connection.commit()

    def insert_columns(self, query, values):
        """
        Function to insert new columns in db
        :param query:
        :return:
        """
        self._connection_cursor(query, values)
        self._connection.commit()

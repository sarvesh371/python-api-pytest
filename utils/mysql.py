__author__ = "sarvesh.singh"

from utils.logger import Logger
import mysql.connector


class MySql:
    """
    MySql Connector for Devx
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
        self.connection_cursor = None
        self._connect_to_db()

    def _connect_to_db(self):
        """
        Function to connect to db
        :return:
        """
        self.logger.debug(
            f"Making Connection to DB with {self.username} {self.password} {self.host} {self.port} {self.database}"
        )
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        self.connection_cursor = self.connection.cursor()

    def run_query(self, query):
        """
        Run db Query Only
        :param query:
        :return:
        """
        self.logger.debug(f"Running SQL Query {query} but not fetching data ...")
        self.connection_cursor.execute(query)

    def run_and_fetch_data(self, query):
        """
        Run db Query and Fetch Data from Database
        :param query:
        :return:
        """
        self.logger.debug(f"Running SQL Query {query} and fetching data ...")
        self.connection_cursor.execute(query)
        return self.connection_cursor.fetchall()

    def delete_data_query(self, table, condition):
        """
        Function to run query to delete data from database
        :param table:
        :param condition:
        :return:
        """
        sql = f"DELETE FROM {table} WHERE {condition}"
        self.connection_cursor.execute(sql)
        self.connection.commit()

    def insert_columns(self, query, values):
        """
        Function to insert new columns in db
        :param query:
        :return:
        """
        self.connection_cursor(query, values)
        self.connection.commit()

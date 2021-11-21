__author__ = "sarvesh.singh"

import logging
import logging.handlers
import os
import sys

loggers = dict()


class CustomConsoleFormatter(logging.Formatter):
    """
    Modify the way DEBUG messages are displayed.
    """

    def __init__(self):
        super().__init__(fmt="{levelname} :: {message}", datefmt=None, style="{")

    def format(self, record):
        # Remember the original format
        format_orig = self._style._fmt

        if record.levelno == logging.INFO:
            self._style._fmt = "{levelname} -> {message}"
        else:
            self._style._fmt = "{filename} {lineno} {levelname} -> {message}"

        result = logging.Formatter.format(self, record)

        # Restore the original format
        self._style._fmt = format_orig

        return result


class Logger:
    """
    Class to initialise the Logging
    # "%(asctime)s %(name)3s %(levelname)-8s %(filename)13s: %(lineno)4d :: %(message)s")
    """

    def __init__(self, name="Automation", level=None):
        """
        Init Function for Logging
        :param name:
        :param level:
        """
        self.name = str(name).upper()
        self.mappings = {
            "DEBUG": logging.DEBUG,  # 10
            "INFO": logging.INFO,  # 20
            "WARNING": logging.WARN,  # 30
            "WARN": logging.WARNING,  # 30
            "ERROR": logging.ERROR,  # 40
            "CRITICAL": logging.CRITICAL,  # 50
        }

        # Set Logging Level: First from environment else
        if level is None:
            self.log_level = self.mappings[os.getenv("LOG_LEVEL", "INFO")]
        else:
            self.log_level = self.mappings[level]

        global loggers
        if loggers.get(self.name):
            self.rootLogger = loggers[self.name]
        else:
            self.rootLogger = logging.getLogger(self.name)

            # Console logs are always set to Info Level to avoid Bombs
            console = logging.StreamHandler(sys.stdout)
            console.setFormatter(CustomConsoleFormatter())
            console.setLevel(logging.INFO)

            self.rootLogger.addHandler(console)
            self.rootLogger.setLevel(self.log_level)

            loggers[self.name] = self.rootLogger

    @property
    def get_logger(self):
        """
        Function that will return logger object
        :return:
        """
        return self.rootLogger

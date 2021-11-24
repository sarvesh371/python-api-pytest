__author__ = "sarvesh.singh"

from slack import WebClient
from utils.logger import Logger


class SlackNotification(WebClient):
    """
    Slack Client to send slack messages
    """

    def __init__(self):
        """
        Slack Web Client Init Function
        """
        self._logger = Logger
        token = ""
        super().__init__(token=token)

    def send_message(self, message, channel=None):
        """
        Send a message to a channel
        :param message: Message to be sent
        :param channel: Channel to which message has to be sent
        :return:
        """
        self.chat_postMessage(channel=channel, text=message)

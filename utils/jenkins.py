__author__ = 'sarvesh.singh'

import time
from utils.common import send_get_request, send_post_request
from utils.logger import Logger

logger = Logger(name='JENKINS').get_logger


class Jenkins:
    """
    Class to perform Jenkins actions
    """

    _job_details = '{}/job/{}/api/json?tree=allBuilds[*]&depth=2'
    _delete_url = '{}/job/{}/{}/doDelete'
    _config_logs_url = '{}/job/{}/{}/consoleText'
    _build_with_params_url = '{}/job/{}/buildWithParameters'
    _build_details = '{}/job/{}/{}/api/json'
    _last_build = '{}/job/{}/lastBuild/api/json'
    _build = '{}/job/{}/{}/api/json'
    _last_success_build = '{}/job/{}/lastSuccessfulBuild/api/json'
    _queue_item = "{}/queue/item/{}/api/json"

    def __init__(self, base_url, token):
        """
        Init Class to initialise jenkins
        :param base_url:
        :param token:
        """
        logger.debug('Connecting to jenkins !!')
        self.base_url = base_url
        super().__init__()
        self.headers = dict()
        self.headers.update({'Authorization': f'Basic {token}'})

    def delete_build(self, name, number):
        """
        Function to delete build
        :param name:
        :param number:
        :return:
        """
        url = self._delete_url.format(self.base_url, name, number)
        send_post_request(url=url, headers=self.headers)
        logger.debug(f'Build # {number} of {name} Deleted !!')

    def get_all_builds(self, name):
        """
        Get all builds of a Job
        :param name:
        :return:
        """
        url = self._job_details.format(self.base_url, name)
        _content = send_get_request(url=url, headers=self.headers)
        return _content['allBuilds']

    def get_build(self, name, number):
        """
        Get a build of a job
        :param name:
        :param number:
        :return:
        """
        url = self._build.format(self.base_url, name, number)
        _content = send_get_request(url=url, headers=self.headers)
        return _content

    def poll_build(self, name, number, fail=True, poll_seconds=1800):
        """
        Poll the build until the result !=None
        :param name:
        :param number:
        :param fail:
        :param poll_seconds:
        :return:
        """
        t_end = time.time() + poll_seconds
        while time.time() < t_end:
            logger.debug('Build is in progress retrying in 3 seconds !!')
            time.sleep(3)
            _content = self.get_build(name=name, number=number)
            if _content['result'] is not None:
                if fail and _content['result'] == 'FAILURE':
                    logger.error(f"Build failed please check: {_content['url']}")
                    raise Exception(f"Build failed please check: {_content['url']}")
                if _content['result'] == 'SUCCESS':
                    return True
        logger.error(f"Build Did not succeed in {poll_seconds} seconds, please check: {_content['url']}")
        raise Exception(f"Build Did not succeed in {poll_seconds} seconds, please check: {_content['url']}")

    def get_console_logs(self, name, number):
        """
        Function to Get Console Logs of a build
        :param name:
        :param number:
        :return:
        """
        url = self._config_logs_url.format(self.base_url, name, number)
        _content = send_get_request(url=url, headers=self.headers)
        return _content

    def get_build_params(self, name, number):
        """
        Get Build Parameters
        :param name:
        :param number:
        :return:
        """
        url = self._build_details.format(self.base_url, name, number)
        _content = send_get_request(url=url, headers=self.headers)
        for action in _content['actions']:
            if '_class' in action:
                if action['_class'] == 'hudson.model.ParametersAction':
                    return {x['name']: x['value'] for x in action['parameters']}

    def rebuild_job(self, name, number):
        """
        Rebuild a Job
        :param name:
        :param number:
        :return:
        """
        params = self.get_build_params(name, number)
        url = self._build_with_params_url.format(self.base_url, name)
        send_post_request(url=url, headers=self.headers, params=params)

    def get_last_build(self, name):
        """
        Get Last Build of a Job
        :param name:
        :return:
        """
        url = self._last_build.format(self.base_url, name)
        _content = send_get_request(url=url, headers=self.headers)
        return _content

    def get_last_successful_build(self, name):
        """
        Get Last Successful Build of a Job
        :param name:
        :return:
        """
        url = self._last_success_build.format(self.base_url, name)
        _content = send_get_request(url=url, headers=self.headers)
        return _content

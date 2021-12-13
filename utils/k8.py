__author__ = 'sarvesh.singh'

import kubernetes
from utils.logger import Logger

logger = Logger(name='K8').get_logger


class K8:
    """
    Class for Kubernetes !!
    """

    def __init__(self, region='us-east-1'):
        """
        Connect to K8 Cluster
        :param region:
        """
        logger.debug('Connecting to k8 !!')
        self._region = region
        self._aws_keys = None

        # Load kube Config
        kubernetes.config.load_kube_config()
        self.client = kubernetes.client.CoreV1Api()
        self.params = {'pretty': 'pretty_example'}

    def get_all_pods(self, namespace=None, fetch_all=False):
        """
        Get all Pods in a namespace
        :param namespace: Namespace from which pods to be fetched
        :param fetch_all: Fetch all Pods, even Scaled and Stopped Ones
        :return:
        """
        _pods = []
        for _pod in self.client.list_namespaced_pod(namespace=namespace).items:
            if fetch_all:
                _pods.append(_pod.metadata.name)
            else:
                if _pod.status.phase in ['Running', 'Succeeded']:
                    _pods.append(_pod.metadata.name)
                else:
                    logger.debug(
                        f'{namespace} Pod {_pod.metadata.name} is in {_pod.status.phase} !!')

        if len(_pods) == 0:
            raise Exception(f'Found Zero Pods for {namespace}- namespace !!')

        return _pods

    def get_all_services(self, namespace=None):
        """
        Get all Services in a namespace
        :param namespace: Namespace from which pods to be fetched
        :return:
        """
        _services = []
        for _service in self.client.list_namespaced_service(namespace=namespace).items:
            _services.append(_service.metadata.name)

        if len(_services) == 0:
            raise Exception(f'Found Zero Services for {namespace}- namespace !!')

        return _services

    def get_logs_for_pod(self, namespace=None, pod_name=None, duration=None):
        """
        Get Logs for a given Pod
        :param namespace:
        :param pod_name:
        :param duration:
        :return:
        """
        if duration:
            self.params['since_seconds'] = str(duration)

        try:
            logs = self.client.read_namespaced_pod_log(pod_name, namespace, **self.params)
        except (Exception, KeyError, ValueError):
            logger.error(f'Failed to Get Pod: {pod_name} Logs !!')
            return []

        return logs

    def delete_pod(self, namespace=None, pod_name=None):
        """
        Delete a Name-spaced Pod
        :param namespace:
        :param pod_name:
        """
        self.client.delete_namespaced_pod(name=pod_name, namespace=namespace)

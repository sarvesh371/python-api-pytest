__author__ = 'sarvesh.singh'

import os
import boto3
import botocore
from utils.logger import Logger

logger = Logger(name='AWS').get_logger


class Aws:
    """
    Class for AWS !!
    """

    def __init__(self):
        """
        Connect to AWS
        """
        logger.debug('Connecting to AWS !!')
        self._aws_keys = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']
        self.check_keys_exported()
        self._s3_resource = boto3.resource('s3')
        self._ec2_client = boto3.client('ec2')
        self._ec2_resource = boto3.resource('ec2')
        self._rds_client = boto3.client('rds')
        self._route53_client = boto3.client('route53')

    def check_keys_exported(self):
        """
        Func to check if aws keys exported
        """
        for _key in self._aws_keys:
            if _key not in os.environ:
                logger.error(f'{_key} does not exist in environment variables !!')
                raise Exception(f'{_key} does not exist in environment variables !!')

    def get_all_buckets(self):
        """
        Func to get all available buckets
        """
        _buckets = []
        for _bucket in self._s3_resource.buckets.all():
            _buckets.append(_bucket)

        return _buckets

    def get_bucket_object(self, bucket_name=None, key=None):
        """
        Func to get the bucket object
        :param bucket_name
        :param key
        """
        obj = self._s3_resource.Object(bucket_name=bucket_name, key=key)
        return obj

    def get_all_instances(self):
        """
        Func to get all ec2 instances
        """
        _instances = []
        for _instance in self._ec2_client.describe_instances()['Reservations']:
            _instances.append(_instance['Instances'][0])

        return _instances

    def get_instance(self, instance_id=None):
        """
        Func to get an instance using instance id
        :param instance_id
        """
        _instance = self._ec2_resource.Instance(instance_id)
        return _instance

    def run_instance(self, ami_id=None, instance_type=None):
        """
        Run an EC2 instance
        :param ami_id:
        :param instance_type:
        :return:
        """
        response = self._ec2_client.run_instances(ImageId=ami_id, InstanceType=instance_type,
                                                  MaxCount=1, MinCount=1)
        _instance = response['Instances'][0]
        return _instance

    def start_instance(self, instance_id=None):
        """
        Start an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Start an instance
            self._ec2_client.start_instances(InstanceIds=[instance_id], DryRun=False)
            logger.debug(f'Successfully started instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                logger.error('Invalid Instance id !!')
            else:
                raise Exception(f'{instance_id} starting failed !!')

    def stop_instance(self, instance_id=None):
        """
        Stop an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Stop an instance
            self._ec2_client.stop_instances(InstanceIds=[instance_id], DryRun=False)
            logger.debug(f'Successfully stopped instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                logger.error('Invalid Instance id !!')
            else:
                raise Exception(f'{instance_id} stopping failed !!')

    def reboot_instance(self, instance_id=None):
        """
        Reboot an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Reboot an instance
            self._ec2_client.reboot_instances(InstanceIds=[instance_id], DryRun=False)
            logger.debug(f'Successfully rebooted instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                logger.error('Invalid Instance id !!')
            else:
                raise Exception(f'{instance_id} rebooting failed !!')

    def terminate_instance(self, instance_id=None):
        """
        Terminate an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Terminate an instance
            self._ec2_client.terminate_instances(InstanceIds=[instance_id], DryRun=False)
            logger.debug(f'Successfully terminated instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Error: Invalid instance id!!")
            else:
                raise Exception(f'{instance_id} termination failed !!')

    def get_all_rds(self):
        """
        Func to get all rds
        """
        _rds = []
        for _db in self._rds_client.describe_db_instances()['DBInstances']:
            _rds.append(_db)

        return _rds

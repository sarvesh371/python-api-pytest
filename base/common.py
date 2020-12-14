__author__ = "sarvesh.singh"

import os
from urllib.parse import urlparse, urlunparse
import re
import requests
from pathlib import Path
from json import (
    dumps as json_dumps,
    load as json_load,
    loads as json_loads,
)
from types import SimpleNamespace as Namespace
import allure
import random
from faker import Faker
from datetime import datetime
import pytz


def urljoin(*args):
    """
    This function will join a URL and return back proper url
    :return:
    """
    parsed = list(urlparse("/".join(args)))
    parsed[2] = re.sub("/{2,}", "/", parsed[2])
    _host = urlunparse(parsed)
    return _host


def read_json_file(file_name, nt=True):
    """
    This function will read Json and return it back in Named-Tuples format
    :param file_name
    :param nt
    """
    if not os.path.isfile(file_name):
        raise Exception(f"File {file_name} Does Not Exist !!")

    with open(file_name, "r") as _fp:
        if nt:
            data = json_load(_fp, object_hook=lambda d: Namespace(**d))
        else:
            data = json_load(_fp)

    return data


def get_resource_config():
    """
    Function to Read URL resource config File
    """
    path = Path(__file__).parent.parent / "resources/config.json"
    return read_json_file(path, nt=True)


def is_key_there_in_dict(key, dictionary, empty_check=True, text=None):
    """
    Check if key is there in dictionary
    :param key:
    :param dictionary:
    :param empty_check:
    :param text:
    :return:
    """
    if key not in dictionary:
        if text is None:
            raise Exception(f"'{key}' not found in _content !!")
        else:
            raise Exception(f"'{key}' not found in _content | {text}")
    else:
        if empty_check:
            if isinstance(dictionary[key], (list, tuple, dict)):
                if len(dictionary[key]) == 0:
                    print(f"{key} is empty !!")
            elif dictionary[key] is None:
                pass
            else:
                pass


def send_get_request(url, headers=None, params=None, timeout=None):
    """
    Send simple Post Request
    :param url:
    :param headers:
    :param params:
    :param timeout:
    :return:
    """
    now = datetime.now(pytz.timezone("Asia/Calcutta"))
    name = f"curlCmd_{now.minute}{now.second}{now.microsecond}.json"
    command = create_curl_command(method='GET', headers=headers, url=url, params=params)
    allure.attach(command, name=name, attachment_type=allure.attachment_type.TEXT)
    if timeout:
        response = requests.get(url=url, headers=headers, params=params, timeout=timeout)
    else:
        response = requests.get(url=url, headers=headers, params=params)
    if response.status_code not in [200, 201]:
        save_allure(data=response.content.decode(response.encoding), name='failResponse.json', save_dump=False)
        raise Exception(f'Status code is : {response.status_code} | Error : {response.text}')
    content = response.content.decode(response.encoding)
    save_allure(data=content, name='passResponse.json', save_dump=False)
    if isinstance(content, dict):
        nt = json_loads(json_dumps(content))
    else:
        nt = json_loads(content)
    return nt


def send_post_request(url, headers, json=None, data=None, params=None):
    """
    Send simple Post Request
    :param url:
    :param json:
    :param headers:
    :param data:
    :param params:
    :return:
    """
    now = datetime.now(pytz.timezone("Asia/Calcutta"))
    name = f"curlCmd_{now.minute}{now.second}{now.microsecond}.json"
    command = create_curl_command(method='POST', headers=headers, url=url, params=params, data=json)
    allure.attach(command, name=name, attachment_type=allure.attachment_type.TEXT)
    response = requests.post(url=url, json=json, data=data, headers=headers, params=params)
    if response.status_code not in [200, 201]:
        save_allure(data=response.content.decode(response.encoding), name='failResponse.json', save_dump=False)
        raise Exception(f'Status code is : {response.status_code} | Error : {response.text}')
    content = response.content.decode(response.encoding)
    save_allure(data=content, name='passResponse.json', save_dump=False)
    if isinstance(content, dict):
        nt = json_loads(json_dumps(content))
    else:
        nt = json_loads(content)
    return nt


def send_put_request(url, headers, json=None, data=None, params=None):
    """
    Send simple Put Request
    :param url:
    :param json:
    :param headers:
    :param data:
    :param params:
    :return:
    """
    now = datetime.now(pytz.timezone("Asia/Calcutta"))
    name = f"curlCmd_{now.minute}{now.second}{now.microsecond}.json"
    command = create_curl_command(method='PUT', headers=headers, url=url, params=params, data=json)
    allure.attach(command, name=name, attachment_type=allure.attachment_type.TEXT)
    response = requests.put(url=url, json=json, data=data, headers=headers, params=params)
    if response.status_code not in [200, 201]:
        save_allure(data=response.content.decode(response.encoding), name='failResponse.json', save_dump=False)
        raise Exception(f'Status code is : {response.status_code} | Error : {response.text}')
    content = response.content.decode(response.encoding)
    save_allure(data=content, name='passResponse.json', save_dump=False)
    if isinstance(content, dict):
        nt = json_loads(json_dumps(content))
    else:
        nt = json_loads(content)
    return nt


def send_delete_request(url, headers, params=None):
    """
    Send simple Delete Request
    :param url:
    :param headers:
    :param params:
    :return:
    """
    now = datetime.now(pytz.timezone("Asia/Calcutta"))
    name = f"curlCmd_{now.minute}{now.second}{now.microsecond}.json"
    command = create_curl_command(method='DELETE', headers=headers, url=url, params=params)
    allure.attach(command, name=name, attachment_type=allure.attachment_type.TEXT)
    response = requests.delete(url=url, headers=headers, params=params)
    if response.status_code not in [200, 201]:
        save_allure(data=response.content.decode(response.encoding), name='failResponse.json', save_dump=False)
        raise Exception(f'Status code is : {response.status_code} | Error : {response.text}')
    content = response.content.decode(response.encoding)
    save_allure(data=content, name='passResponse.json', save_dump=False)
    if isinstance(content, dict):
        nt = json_loads(json_dumps(content))
    else:
        nt = json_loads(content)
    return nt


def save_allure(data, name, save_dump=True):
    """
    Save allure report by converting data to Json
    :param data:
    :param name:
    :param save_dump:
    :type name:
    :return:
    """
    if len(data) != 0:
        if isinstance(data, str):
            name = str(name).replace(".json", ".log")
            allure.attach(data, name=name, attachment_type=allure.attachment_type.TEXT)
            if save_dump:
                with open(name, "w") as _fp:
                    _fp.write(data)
            return str
        else:
            dump = json_dumps(data, indent=2, sort_keys=True)
            allure.attach(dump, name=name, attachment_type=allure.attachment_type.JSON)
            if save_dump:
                with open(name, "w") as _fp:
                    _fp.write(dump)
            return dump


def generate_phone_number(max_digits=10):
    """
    Function to generate phone number
    :param max_digits:
    :return:
    """
    return random.randint(10 ** (max_digits - 1), 10 ** max_digits - 1)


def generate_email_id(**kwargs):
    """
    Function to generate Email ID
    :return:
    """
    tail = f"_{str(generate_phone_number(6))}@thinxnet.com"
    email_id = re.sub(
        r"(.*?)@.*", r"\1{}".format(tail), str(Faker().email()), re.I | re.M
    )
    return str(email_id).lower()


def create_curl_command(method, headers, url, params=None, data=None):
    """
    Create the curl command which is being Hit !!
    :param method:
    :param headers:
    :param url:
    :param params:
    :param data:
    :return:
    """
    # Check if data is in Json/dict format, convert it into string after that
    if isinstance(data, dict) or isinstance(data, list):
        data = json_dumps(data)
    headers = " --header ".join(
        [
            f'"{k}: {v}"'
            for k, v in headers.items()
            if k not in ["User-Agent", "Accept-Encoding"]
        ]
    )

    if params:
        url = f'{url}?{"&".join([f"{k}={v}" for k, v in params.items()])}'

    if data:
        command = f"curl --request {method} --include --silent --show-error --header {headers} --data '{data}' '{url}'"
    else:
        command = f"curl --request {method} --include --silent --show-error --header {headers} '{url}'"

    # We always save Curl Command in environment variable, so that we know (in-case) of an exception what was it.
    os.environ["CURL"] = command
    return command

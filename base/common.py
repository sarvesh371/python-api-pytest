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
    data = Path(__file__).parent.parent / "resources/config.json"
    return read_json_file(data, nt=True)


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
    if timeout:
        response = requests.request(
            "GET", url, headers=headers, params=params, timeout=timeout, verify=False
        )
    else:
        response = requests.request(
            "GET", url, headers=headers, params=params, verify=False
        )
    content = response.content.decode("utf-8")
    if isinstance(content, dict):
        nt = json_loads(json_dumps(content))
    else:
        nt = json_loads(content)
    return nt


def send_post_request(url, data, headers, params=None):
    """
    Send simple Post Request
    :param url:
    :param data:
    :param headers:
    :param params:
    :return:
    """
    response = requests.request(
        "POST", url, data=data, headers=headers, params=params, verify=False
    )
    content = response.content.decode("utf-8")
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
    response = requests.request(
        "DELETE", url, headers=headers, params=params, verify=False
    )
    content = response.content.decode("utf-8")
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

__author__ = "sarvesh.singh"

from base.common import get_resource_config
import os
import pytest


def pytest_configure(config):
    """
    Configuration changes for PyTest
    :param config:
    :return:
    """
    os.environ["ROOT_PATH"] = config.rootdir.strpath
    config.option.cacheclear = True
    config.option.capture = "sys"  # no: for no output at all
    config.option.clean_alluredir = True
    config.option.color = "yes"
    config.option.disable_warnings = True
    config.option.instafail = True
    config.option.failedfirst = True
    config.option.json_report_indent = 2
    config.option.json_report_omit = ["warnings"]
    config.option.json_report = True
    config.option.maxfail = 1
    config.option.pythonwarnings = ["ignore:Unverified HTTPS request"]
    config.option.tbstyle = "short"
    config.option.self_contained_html = True
    config.option.verbose = 1

    if config.getoption("allure_report_dir") is None:
        config.option.allure_report_dir = f"allure-results"

    if config.getoption("json_report_file") == ".report.json":
        config.option.json_report_file = f"report.json"

    if config.getoption("htmlpath") is None:
        config.option.htmlpath = f"report.html"

    if config.getoption("xmlpath") is None:
        config.option.xmlpath = f"report.xml"


@pytest.fixture(autouse=True, scope="session")
def resources():
    """
    resources Fixture with all Url
    :return:
    """
    return get_resource_config()


@pytest.fixture(autouse=True, scope="session")
def test_data():
    """
    Create a dict and write every test data there
    :return:
    """
    test_data = dict()
    return test_data

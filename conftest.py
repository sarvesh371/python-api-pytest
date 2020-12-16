__author__ = "sarvesh.singh"

from base.common import read_json_file, read_sample_json
import os
import pytest
from pathlib import Path


def pytest_addoption(parser):
    """
    Adds custom command line options for running configurable code
    :param parser:
    :return:
    """
    parser.addoption("--base-url", action="store", default='http://localhost:3000', help="Base URL")


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
def config(request):
    """
    Create a dict() and save the configuration there
    :param request
    :return:
    """
    config = {
        'baseUrl': request.config.getoption("--base-url"),
    }
    return config


@pytest.fixture(scope="session")
def test_data():
    """
    Create a dict and write every test data there
    :return:
    """
    test_data = dict()
    return test_data


@pytest.fixture(scope="session")
def tear_down_fixture(test_data):
    """
    Tear down fixture
    :param test_data: Test Data Fixture
    """
    yield
    test_data['summary'] = dict()
    test_data['summary']['status'] = 'Pass'
    path = Path(__file__).parent / "report.json"
    report = read_json_file(path, nt=True)
    test_data['summary']['total'] = report.summary.collected
    test_data['summary']['failed'] = report.summary.failed
    test_data['summary']['passed'] = report.summary.total - report.summary.failed
    if bool(test_data['summary']['failed']):
        test_data['summary']['status'] = 'Fail'


@pytest.fixture(scope="session")
def sample_json():
    """
    Fetch all sample json and convert it to name tuple .
    :return:
    """
    json_data = read_sample_json()
    return json_data

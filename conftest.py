__author__ = "sarvesh.singh"

from base.common import read_sample_json, update_allure_environment, computing_test_result, \
    send_slack_webhook

import os
import pytest
from json import (
    dumps as json_dumps,
    load as json_load,
)

# Global variable
results = list()


def pytest_addoption(parser):
    """
    Adds custom command line options for running configurable code
    :param parser:
    :return:
    """
    parser.addoption("--env", action="store", default='local', help="Environment")
    parser.addoption("--report", action="store_true", default=False, help="Send Result")


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
    config = dict()
    if request.config.getoption("--env") == 'local':
        config.update({
            'baseUrl': 'http://localhost:3000'
        })
    return config


@pytest.fixture(autouse=True)
def set_allure_environment(request, config):
    """
    Fixture to set environment in allure report
    :param request:
    :param config:
    :return:
    """
    update_allure_environment(request, config)


@pytest.fixture(scope="session")
def test_data():
    """
    Create a dict and write every test data there
    :return:
    """
    test_data = dict()
    return test_data


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Fixture to get the result of test case
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == 'setup':
        pass
    elif report.when == 'call':
        if report.outcome == 'passed':
            result = {
                "testName": item.name,
                "result": report.outcome,
            }
        else:
            result = {
                "testName": item.name,
                "result": report.outcome,
                'error': ''.join(call.excinfo.value.args),
            }
        global results
        results.append(result)
        # saving each test case result
        with open("results.json", "w+") as _fp:
            _fp.write(json_dumps(results, default=lambda o: o.__dict__, indent=2, sort_keys=True))
    elif report.when == 'teardown':
        pass


@pytest.fixture(autouse=True, scope="session")
def tear_down_fixture(test_data, request):
    """
    Tear down fixture and send Slack message
    :param test_data: Test Data Fixture
    :param request: pytest request
    """
    yield
    # dump test_data.json
    with open("test_data.json", "w+") as _fp:
        _fp.write(json_dumps(test_data, default=lambda o: o.__dict__, indent=2, sort_keys=True))

    # collecting test results
    with open('results.json', "r") as _fp:
        result = json_load(_fp)

    # computing test result
    status, total_tests, executed, passed = computing_test_result(request=request, result=result)

    # Sending slack message
    if request.config.getoption("--report"):
        allure_link = f"{os.environ.get('BUILD_URL')}allure"
        send_slack_webhook(status, total_tests, executed, passed, allure_link)


@pytest.fixture(autouse=True, scope="session")
def sample_json():
    """
    Fetch all sample json and convert it to name tuple .
    :return:
    """
    json_data = read_sample_json()
    return json_data

__author__ = "sarvesh.singh"

from base.common import get_resource_config
import os
import pytest


def pytest_addoption(parser):
    """
    Adds custom command line options for running the pytest harness
    All options will be stored in pytest config
    :param parser:
    :return:
    """
    parser.addoption("--url", action="store", default=None, help="URL")


def pytest_sessionstart(session):
    """
    Hook to be executed before session starts and before collection
    :param session:
    :return:
    """
    pass


def pytest_sessionfinish(session, exitstatus):
    """
    Hook to be executed after tests execution and session is about to end
    :param session:
    :param exitstatus:
    :return:
    """
    pass


def pytest_report_teststatus(report, config):
    """
    Hook for Test Status Report
    :param report:
    :param config:
    :return:
    """
    pass


def pytest_internalerror(excrepr, excinfo):
    """
    Hook if there is any internal error
    :param excrepr:
    :param excinfo:
    :return:
    """
    pass


def pytest_keyboard_interrupt(excinfo):
    """
    Hook Called when there is a Keyboard Interrupt
    :param excinfo:
    :return:
    """
    pass


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


def pytest_runtest_setup(item):
    """
    Runs Before pytest_runtest_call
    :param item:
    """
    pass


def pytest_runtest_call(item):
    """
    Called to execute the Test item
    :param item:
    :param nextitem:
    """
    pass


def pytest_runtest_teardown(item, nextitem):
    """
    Runs after pytest_runtest_call
    :param item:
    :param nextitem:
    """
    pass


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This is a run into the report generated after a test case
    is done executing
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    report = outcome.get_result()


@pytest.fixture(autouse=True, scope="session")
def tear_down_fixture(request):
    """
    Teardown Fixture
    :param request:
    :return:
    """
    yield


@pytest.fixture(autouse=True, scope="session")
def resources():
    """
    resources Fixture with all Url
    :return:
    """
    return get_resource_config()

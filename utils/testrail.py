__author__ = 'sarvesh.singh'

from testrail_api import TestRailAPI
from utils.logger import Logger

logger = Logger(name='TESTRAIL').get_logger


class TestRail:
    """
    Class for Test Rail !!
    """

    def __init__(self, url=None, email=None, password=None):
        """
        Connect to Test Rail
        :param url
        :param email
        :param password
        :return:
        """
        logger.debug('Connecting to testrail !!')
        self._api = TestRailAPI(url=url, email=email, password=password)

    def get_projects(self):
        """
        Get all projects
        :return:
        """
        _projects = self._api.projects.get_projects()
        return _projects['projects']

    def get_project(self, project_id=None):
        """
        Get Project
        :param project_id:
        :return:
        """
        _project = self._api.projects.get_project(project_id=project_id)
        return _project

    def get_suites(self, project_id=None):
        """
        Get Suites
        :param project_id:
        :return:
        """
        _suites = self._api.suites.get_suites(project_id=project_id)
        return _suites

    def get_suite(self, suite_id=None):
        """
        Get Suite
        :param suite_id:
        :return:
        """
        _suite = self._api.suites.get_suite(suite_id=suite_id)
        return _suite

    def add_suite(self, project_id, suite_name=None):
        """
        Add Suite
        :param project_id:
        :param suite_name:
        :return:
        """
        _suite = self._api.suites.add_suite(project_id=project_id, name=suite_name)
        return _suite

    def get_milestones(self, project_id=None):
        """
        Get all milestones
        :param project_id:
        :return:
        """
        _milestones = self._api.milestones.get_milestones(project_id=project_id)
        return _milestones['milestones']

    def get_milestone(self, milestone_id=None):
        """
        Get milestone
        :param milestone_id:
        :return:
        """
        _milestone = self._api.milestones.get_milestone(milestone_id=milestone_id)
        return _milestone

    def get_plans(self, project_id=None):
        """
        Get all plans
        :param project_id:
        :return:
        """
        _plans = self._api.plans.get_plans(project_id=project_id)
        return _plans['plans']

    def get_plan(self, plan_id=None):
        """
        Get plan
        :param plan_id:
        :return:
        """
        _plan = self._api.plans.get_plan(plan_id=plan_id)
        return _plan

    def add_plan(self, project_id=None, suite_id=None, name=None, case_ids=None):
        """
        Add plan with provided case id's
        :param project_id:
        :param suite_id:
        :param name:
        :param case_ids:
        :return:
        """
        _kwargs = {
            'entries': [
                {
                    'suite_id': suite_id,
                    'include_all': False,
                    'case_ids': case_ids
                }
            ]
        }
        _plan = self._api.plans.add_plan(project_id=project_id, name=name, **_kwargs)
        return _plan

    def close_plan(self, plan_id=None):
        """
        Close plan
        :param plan_id:
        :return:
        """
        _plan = self._api.plans.close_plan(plan_id=plan_id)
        return _plan

    def delete_plan(self, plan_id=None):
        """
        Delete plan
        :param plan_id:
        :return:
        """
        self._api.plans.delete_plan(plan_id=plan_id)

    def get_runs(self, project_id=None):
        """
        Get all runs
        :param project_id:
        :return:
        """
        _runs = self._api.runs.get_runs(project_id=project_id)
        return _runs['runs']

    def get_run(self, run_id=None):
        """
        Get run
        :param run_id:
        :return:
        """
        _run = self._api.runs.get_run(run_id=run_id)
        return _run

    def add_run(self, project_id=None, suite_id=None, name=None, case_ids=None):
        """
        Add run
        :param project_id:
        :param suite_id:
        :param name:
        :param case_ids:
        :return:
        """
        _kwargs = {
            'suite_id': suite_id,
            'name': name,
            'include_all': False,
            'case_ids': case_ids
        }
        _run = self._api.runs.add_run(project_id=project_id, **_kwargs)
        return _run

    def close_run(self, run_id=None):
        """
        Close run
        :param run_id:
        :return:
        """
        _run = self._api.runs.close_run(run_id=run_id)
        return _run

    def delete_run(self, run_id=None):
        """
        Delete run
        :param run_id:
        :return:
        """
        self._api.runs.delete_run(run_id=run_id)

    def get_tests(self, run_id=None):
        """
        Get tests
        :param run_id:
        :return:
        """
        _tests = self._api.tests.get_tests(run_id=run_id)
        return _tests

    def get_test(self, test_id=None):
        """
        Get test
        :param test_id:
        :return:
        """
        _test = self._api.tests.get_test(test_id=test_id)
        return _test

    def get_cases(self, project_id=None, suite_id=None):
        """
        Get cases
        :param project_id:
        :param suite_id:
        :return:
        """
        _kwargs = {
            'suite_id': suite_id
        }
        _cases = self._api.cases.get_cases(project_id=project_id, **_kwargs)
        return _cases['cases']

    def get_case(self, case_id=None):
        """
        Get case
        :param case_id:
        :return:
        """
        _case = self._api.cases.get_case(case_id=case_id)
        return _case

    def add_case_result(self, run_id=None, case_id=None, status=None, comment=None):
        """
        Add case result
        1	Passed
        2	Blocked
        3	Untested (not allowed when adding a result)
        4	Retest
        5	Failed
        :param case_id:
        :param run_id:
        :param status:
        :param comment:
        :return:
        """
        _kwargs = {
            'status_id': status,
            'comment': comment
        }
        _result = self._api.results.add_result_for_case(run_id=run_id, case_id=case_id, **_kwargs)

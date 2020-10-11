__author__ = "sarvesh.singh"

import pytest
from base.common import *


@pytest.mark.REST
@pytest.mark.run(order=1)
class TestRest:
    """
    This suite is created to test the User and employee flow
    """

    def test_01_register_user(self, resources, test_data):
        """
        Register User
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.register)
        email_id = generate_email_id(from_saved=True, first_name='Sarvesh', last_name='Singh')
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "company": {
                "company_name": "thinxnet",
                "company_phone": "123",
                "company_street": "Second Street",
                "company_house_number": "92",
                "company_postcode": "321001",
                "company_city": "munich",
                "company_county": "German",
                "company_country": "Germany",
                "company_account_status": "45",
                "payment_id": 1,
                "plan_id": 12
            },
            "user": {
                "email": email_id,
                "password": "Yellow*99",
                "role_id": 1,
                "company_id": 23
            }
        }
        response = send_post_request(url, json=body, headers=headers)
        save_allure(data=response, name='registerUser', save_dump=False)
        test_data['user'] = dict()
        # To check the keys of API's
        is_key_there_in_dict('status', response)
        assert 'success' == response['status'], 'Status is not success !!'
        is_key_there_in_dict('data', response)
        test_data['user'] = response['data']
        is_key_there_in_dict('role_id', response['data'])
        is_key_there_in_dict('company_id', response['data'])
        is_key_there_in_dict('email', response['data'])
        is_key_there_in_dict('id', response['data'])

    def test_02_login_user(self, resources, test_data):
        """
        Verify User is able to login
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.login)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'email': test_data['user']['email'],
            'password': 'Yellow*99'
        }
        response = send_post_request(url, data=body, headers=headers)
        save_allure(data=response, name='loginUser', save_dump=False)
        is_key_there_in_dict('status', response)
        assert 'success' == response['status'], 'Status is not success !!'
        is_key_there_in_dict('data', response)
        is_key_there_in_dict('token', response['data'])
        is_key_there_in_dict('user', response['data'])
        is_key_there_in_dict('type', response['data']['token'])
        is_key_there_in_dict('token', response['data']['token'])
        is_key_there_in_dict('refreshToken', response['data']['token'])
        test_data['user']['token'] = f"{response['data']['token']['type']} {response['data']['token']['token']}"

    def test_03_create_employee_error(self, resources, test_data):
        """
        Show the error which we are getting while creating employee by following docs
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.createEmployee)
        email_id = generate_email_id(from_saved=True, first_name='Sarvesh', last_name='Singh')
        id = generate_phone_number(7)
        headers = {
            'Authorization': test_data['user']['token'],
            'Content-Type': 'application/json'
        }
        body = {
            "profile": {
                "role": "admin",
                "id": id,
                "employee_email": email_id,
                "password": "Yellow*99"
            }
        }
        try:
            response = send_post_request(url, json=body, headers=headers)
        except Exception as exp:
            save_allure(data=exp.args[0], name='createEmployeeError', save_dump=False)
            pytest.xfail(reason='Employee Name field is not default null !!')

    def test_04_create_employee(self, resources, test_data):
        """
        Fix the error in above test case and create employee
        :param resources
        :param test_data
        :return:
        """
        test_data['employee'] = dict()
        url = urljoin(resources.baseUrl, resources.createEmployee)
        test_data['employee']['emailIid'] = generate_email_id(from_saved=True, first_name='Sarvesh', last_name='Singh')
        test_data['employee']['id'] = generate_phone_number(7)
        headers = {
            'Authorization': test_data['user']['token'],
            'Content-Type': 'application/json'
        }
        body = {
            "profile": {
                "role": "admin",
                "id": test_data['employee']['id'],
                "employee_email": test_data['employee']['emailIid'],
                "employee_name": "Sarvesh",
                "password": "Yellow*99"
            }
        }
        response = send_post_request(url, json=body, headers=headers)
        save_allure(data=response, name='createEmployee', save_dump=False)
        is_key_there_in_dict('status', response)
        assert 'success' == response['status'], 'Status is not success !!'
        is_key_there_in_dict('message', response)
        assert 'Employee successfully saved. User added also' == response['message'], 'Sucess message is wrong !!'

    def test_05_login_employee(self, resources, test_data):
        """
        Employee login
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.login)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'email': test_data['employee']['emailIid'],
            'password': 'Yellow*99'
        }
        response = send_post_request(url, data=body, headers=headers)
        save_allure(data=response, name='loginEmployee', save_dump=False)
        is_key_there_in_dict('status', response)
        assert 'success' == response['status'], 'Status is not success !!'
        is_key_there_in_dict('data', response)
        is_key_there_in_dict('token', response['data'])
        is_key_there_in_dict('user', response['data'])
        is_key_there_in_dict('type', response['data']['token'])
        is_key_there_in_dict('token', response['data']['token'])
        is_key_there_in_dict('refreshToken', response['data']['token'])
        test_data['employee']['token'] = f"{response['data']['token']['type']} {response['data']['token']['token']}"

    def test_06_get_profile(self, resources, test_data):
        """
        Get employee profile
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.profile)
        headers = {
            'Authorization': test_data['employee']['token'],
            'Content-Type': 'application/json'
        }
        response = send_get_request(url, headers=headers)
        save_allure(data=response, name='getProfile', save_dump=False)
        is_key_there_in_dict('status', response)
        assert 'success' == response['status'], 'Status is not success !!'
        is_key_there_in_dict('data', response)
        is_key_there_in_dict('employee_name', response['data'])
        assert 'Sarvesh' == response['data']['employee_name'], 'Employee name Mismatch !!'
        is_key_there_in_dict('employee_email', response['data'])
        assert test_data['employee']['emailIid'] == response['data']['employee_email'], 'Employee name Mismatch !!'

    def test_07_update_profile(self, resources, test_data):
        """
        Update profile and change Employee Name
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.updateProfile.format(test_data['employee']['id']))
        headers = {
            'Authorization': test_data['employee']['token'],
            'Content-Type': 'application/json'
        }
        body = {
            "id": test_data['employee']['id'],
            "employee_name": "Sarvesh Singh",
            "employee_email": test_data['employee']['emailIid'],
        }
        try:
            response = send_put_request(url, json=body, headers=headers)
        except Exception as exp:
            save_allure(data=exp.args[0], name='updateProfileError', save_dump=False)
            pytest.xfail(reason='Route is not set for Update profile flow !!')

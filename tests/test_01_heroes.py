__author__ = "sarvesh.singh"

import pytest
from base.common import *


@pytest.mark.HEROES
@pytest.mark.run(order=1)
class TestHeroes:
    """
    This suite is created to test the fight and heroes flow
    """

    def test_01_verify_and_get_heroes(self, resources, test_data):
        """
        Get heroes and verify
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.heroesList)
        headers = {
            'Authorization': resources.token
        }
        response = send_get_request(url, headers=headers)
        save_allure(data=response, name='getHeroes', save_dump=False)
        assert len(response) != 0, 'No heroes returned !!'
        test_data['heroes'] = []
        # To check the keys of API's
        for _hero in response:
            is_key_there_in_dict('id', _hero)
            is_key_there_in_dict('name', _hero)
            is_key_there_in_dict('powerlevel', _hero)
            test_data['heroes'].append(_hero)

    def test_02_verify_hero_api(self, resources, test_data):
        """
        Verify api to get one hero using hero id
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.hero.format(test_data['heroes'][0]['id']))
        headers = {
            'Authorization': resources.token
        }
        response = send_get_request(url, headers=headers)
        save_allure(data=response, name='getHero', save_dump=False)
        is_key_there_in_dict('id', response)
        assert len(response) != 0, 'Hero not Found !!'
        assert response['id'] == test_data['heroes'][0]['id'], 'Hero Id mismatch !!'

    def test_03_add_first_hero_fight(self, resources, test_data):
        """
        Add first hero to fight and try to add same hero twice
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.addHero)
        headers = {
            'Authorization': resources.token
        }
        body = {
            "heroId": test_data['heroes'][0]['id'],
        }
        response = send_post_request(url, data=body, headers=headers)
        save_allure(data=response, name='addFirstHero', save_dump=False)
        is_key_there_in_dict('message', response)
        if 'Yippie!' not in response['message']:
            raise Exception(f"{test_data['heroes'][0]['name']} did not get added !!")

        # To check what happens if we add same hero twice
        body = {
            "heroId": test_data['heroes'][0]['id'],
        }
        response = send_post_request(url, data=body, headers=headers)
        save_allure(data=response, name='addFirstHero', save_dump=False)
        is_key_there_in_dict('errorCode', response)
        is_key_there_in_dict('error', response)
        assert response['errorCode'] == '1001', 'Error Code Mis Match !!'
        assert response[
                   'error'] == 'Thor could not be added because is already in the fight.', 'Same Hero added Twice !!'

    def test_04_start_fight(self, resources):
        """
        Start fight with only 1 hero
        :param resources
        :return:
        """
        url = urljoin(resources.baseUrl, resources.fight)
        headers = {
            'Authorization': resources.token
        }
        response = send_post_request(url, data=None, headers=headers)
        save_allure(data=response, name='startFight', save_dump=False)
        is_key_there_in_dict('errorCode', response)
        is_key_there_in_dict('error', response)
        assert response['errorCode'] == '1004', 'Error Code Mis Match !!'
        assert response[
                   'error'] == 'You can not start a fight with less than 2 heroes', 'Fight started with only 1 hero !!'

    def test_05_add_second_hero_fight(self, resources, test_data):
        """
        Add Second hero to fight
        :param resources
        :param test_data
        :return:
        """
        url = urljoin(resources.baseUrl, resources.addHero)
        headers = {
            'Authorization': resources.token
        }
        body = {
            "heroId": test_data['heroes'][1]['id'],
        }
        response = send_post_request(url, data=body, headers=headers)
        save_allure(data=response, name='addSecondHero', save_dump=False)
        is_key_there_in_dict('message', response)
        if 'Yippie!' not in response['message']:
            raise Exception(f"{test_data['heroes'][1]['name']} did not get added !!")

    def test_06_start_fight_with_two_heroes(self, resources):
        """
        Start fight with 2 heroes
        :param resources
        :return:
        """
        url = urljoin(resources.baseUrl, resources.fight)
        headers = {
            'Authorization': resources.token
        }
        response = send_post_request(url, data=None, headers=headers)
        save_allure(data=response, name='startFightAgain', save_dump=False)

    def test_07_reset_fight(self, resources):
        """
        Reset Fight
        :param resources
        :return:
        """
        url = urljoin(resources.baseUrl, resources.fight)
        headers = {
            'Authorization': resources.token
        }
        response = send_delete_request(url, headers=headers)
        save_allure(data=response, name='resetFight', save_dump=False)
        is_key_there_in_dict('message', response)
        assert response[
                   'message'] == 'Fight has been deleted and now all heroes went back to Helicarrier Ship.', 'Fight is not reset !!'

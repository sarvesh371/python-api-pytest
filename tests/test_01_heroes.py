__author__ = "sarvesh.singh"

import pytest


@pytest.mark.HEROES
@pytest.mark.run(order=1)
class TestHeroes:
    """
    This suite is created to test the war and heroes flow
    """

    def test_01_launch_flipkart(self, web_driver, pages):
        """
        Load flipkart website
        :return:
        :param web_driver
        :param pages
        """
        web_driver.allure_attach_jpeg(file_name='homePage')
        pages.home.close_pop_up()

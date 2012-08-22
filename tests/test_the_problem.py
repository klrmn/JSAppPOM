#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException

from JSAppPOM import JSAppPOM


@pytest.mark.nondestructive
class TestPlainPageObject(object):

    class PageObject(object):

        def __init__(self, mozwebqa):
            self.mozwebqa = mozwebqa
            self.selenium = mozwebqa.selenium
            self.timeout = mozwebqa.timeout

        def ajax_has_stopped_now(self):
            return self.selenium.execute_script('return jQuery.active == 0')


    # click tests
    @pytest.mark.parametrize('element', ['button', 'link'])
    def test_click_does_not_wait_for_ajax_to_finish_before_returning(self, mozwebqa, element):
        pom = self.PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, element).click()
        is_running = not pom.ajax_has_stopped_now()
        assert is_running

    @pytest.mark.parametrize('element', ['button', 'link'])
    def test_click_does_not_wait_for_element_to_be_visible(self, mozwebqa, element):
        pom = self.PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, element).click()
        try:
            pom.selenium.find_element(By.ID, 'second_' + element).click()
        except ElementNotVisibleException as e:
            assert e.msg != ""

    # send_keys tests
    def test_send_keys_does_not_wait_for_ajax_to_finish_before_returning(self, mozwebqa):
        pom = self.PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        is_running = not pom.ajax_has_stopped_now()
        assert is_running

    def test_send_keys_does_not_wait_for_element_to_be_visible(self, mozwebqa):
        pom = self.PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        try:
            pom.selenium.find_element(By.ID, 'second_text').send_keys('some other text\t')
        except ElementNotVisibleException as e:
            assert e.msg != ""

    # text tests
    def test_text_does_not_wait_for_element_to_be_visible(self, mozwebqa):
        pom = self.PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'link').click()
        try:
            pom.selenium.find_element(By.ID, 'second_link').text
        except ElementNotVisibleException as e:
            assert e.msg == ""

    # get_attribute tests
    def test_get_attribute_does_not_wait_for_element_to_be_visible(self, mozwebqa):
        pom = self.PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').click()
        try:
            pom.selenium.find_element(By.ID, 'second_text').get_attribute('value')
        except ElementNotVisibleException as e:
            assert e.msg == ""

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException

from JSAppPOM import JSAppPOM


@pytest.mark.nondestructive
class TestJSAppPageObject(object):

    class TestJSAppPOM(JSAppPOM):

        def ajax_active_state(self):
            return self.selenium.execute_script('return jQuery.active')

    # click Tests
    def test_click_waits_for_element_visible_before_clicking(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        # click first element the old way
        pom.selenium.find_element(By.ID, 'button').click()
        # second element will take 10 seconds to appear
        # click second element the new way
        pom.click(By.ID, 'second_button')
        # no ElementNotVisibleException

    def test_click_waits_for_ajax_to_finish_before_returning(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        pom.click(By.ID, 'button')
        assert pom.ajax_active_state() == 0

    def test_click_will_error_if_element_does_not_become_visible(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        try:
            pom.click(By.ID, 'third_button')
        except TimeoutException as e:
            assert "element was not found or did not become visible" in e.msg

    # send_keys tests
    def test_send_keys_waits_for_element_visible_before_typing(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        # type in the first elementt he old way
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        # second element will take 10 seconds to appear
        # type in second element the new way
        pom.send_keys('some new text', By.ID, 'second_text')
        # no ElementNotVisibleException

    def test_send_keys_waits_for_ajax_to_finish_before_returning(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        pom.send_keys('some text\t', By.ID, 'text')
        assert pom.ajax_active_state() == 0

    def test_send_keys_will_error_if_element_does_not_become_visible(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        try:
            pom.send_keys('some text\t', By.ID, 'text')
        except TimeoutException as e:
            assert e.msg != ""
        
    # clear_and_type tests
    def test_clear_and_type_waits_for_element_visible_before_typing(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        # type in the first elementt he old way
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        # second element will take 10 seconds to appear
        # type in second element the new way
        pom.clear_and_type('some new text', By.ID, 'second_text')
        # no ElementNotVisibleException

    def test_clear_and_type_waits_for_ajax_to_finish_before_returning(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        pom.clear_and_type('some text\t', By.ID, 'text')
        assert pom.ajax_active_state() == 0

    def test_clear_and_type_will_error_if_element_does_not_become_visible(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        try:
            pom.clear_and_type('some text\t', By.ID, 'text')
        except TimeoutException as e:
            assert e.msg != ""

    # text tests
    def test_text_waits_for_element_visible(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        pom.selenium.find_element(By.ID, 'link').click()
        # second span will take 10 seconds to appear
        assert pom.text(By.ID, 'second_link') == 'appearing'

    def test_text_errors_if_element_does_not_become_visible(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        try:
            pom.text(By.ID, 'second_span')
        except TimeoutException as e:
            assert e.msg != ""

    # get_attribute tests
    def test_get_attribute_waits_for_element_visible(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').click()
        assert pom.get_attribute('value', By.ID, 'second_text') == 'appearing'

    def test_get_attribute_if_element_does_not_become_visible(self, mozwebqa):
        pom = self.TestJSAppPOM(mozwebqa)
        try:
            pom.get_attribute('value', By.ID, 'second_text')
        except TimeoutException as e:
            assert e.msg != ""


#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.support.ui import WebDriverWait


class JSAppPOM(object):

    def __init__(mozwebqa):
        self.mozwebqa = mozwebqa
        self.selenium = mozwebqa.selenium
        self.timeout  = mozwebqa.timeout

    def wait_for_ajax(self):
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.selenium.execute_script('return jQuery.active == 0'))

    def wait_for_locator(self, *locator):
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*locator) and s.find_element(*locator).is_displayed(),
            "element was not found or did not become visible within %s seconds" % self.timeout)

    def click(self, *locator):
        self.wait_for_locator(*locator)
        self.selenium.find_element(*locator).click()
        self.wait_for_ajax()

    def send_keys(self, value, *locator):
        self.wait_for_locator(*locator)
        self.selenium.find_element(*locator).send_keys(value)
        self.wait_for_ajax()

    @property
    def text(*locator):
        self.wait_for_locator(*locator)
        return self.selenium.find_element(*locator).text

    def get_attribute(*locator, attribute):
        self.wait_for_locator(*locator)
        return self.selenium.find_element(*locator).get_attribute(attribute)

    def clear_and_type(*locator, value):
        self.wait_for_locator(*locator)
        element = self.selenium.find_element(*locator)
        element.clear()
        element.send_keys(value)
        self.wait_for_ajax()

    # XXX methods for checkboxes, radio buttons and select boxes?

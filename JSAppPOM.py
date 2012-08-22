#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.support.ui import WebDriverWait


class JSAppPOM(object):
    '''A Page Object Model base class for pages generated dynamically by javascript.'''

    def __init__(mozwebqa):
        '''JSAppPOM constructor.
        :Args:
        - mozwebqa - as provided by the pytest-mozwebqa plugin, or any object implementing 'selenium' and 'timeout' attributes.
        '''
        self.mozwebqa = mozwebqa
        self.selenium = mozwebqa.selenium
        self.timeout  = mozwebqa.timeout

    def is_visible_now(self, *locator):
        '''Instance Method. Checks to see if the element is displayed right now.
        :Args:
        - locator - a tuple consisting of 
          * a constant from selenium.webdriver.common.by
          * a value
        '''
        self.selenium.implicit_timeout(0)
        answer = self.selenium.find_element(*locator).is_displayed()
        self.selenium.implicit_timeout(self.timeout)
        return answer

    def ajax_has_stopped_now(self):
        '''Instance Method. Checks to see if jQuery is inactive right now.'''
        return self.selenium.execute_script('return jQuery.active == 0')

    def wait_for_ajax(self):
        '''Instance Method. Waits for jQuery to be inactive.'''
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.selenium.execute_script('return jQuery.active == 0'))

    def wait_for_locator(self, *locator):
        '''Instance Method. Waits for locator to be found and displayed.
        :Args:        
        - locator - a tuple consisting of 
          * a constant from selenium.webdriver.common.by
          * a value
        '''
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*locator) and s.find_element(*locator).is_displayed(),
            "element was not found or did not become visible within %s seconds" % self.timeout)

    def click(self, *locator):
        '''Instance Method. Waits for locator, clicks it, then waits for ajax to finish.
        :Args:        
        - locator - a tuple consisting of 
          * a constant from selenium.webdriver.common.by
          * a value
        '''
        self.wait_for_locator(*locator)
        self.selenium.find_element(*locator).click()
        self.wait_for_ajax()

    def send_keys(self, value, *locator):
        '''Instance Method. Waits for locator, sends keys, then waits for ajax to finish.
        :Args:
        - value - keys to send
        - locator - a tuple consisting of 
          * a constant from selenium.webdriver.common.by
          * a value
        '''
        self.wait_for_locator(*locator)
        self.selenium.find_element(*locator).send_keys(value)
        self.wait_for_ajax()

    @property
    def text(*locator):
        '''Instance Method. Waits for locator, then returns the text.
        :Args:        
        - locator - a tuple consisting of 
          * a constant from selenium.webdriver.common.by
          * a value
        '''
        self.wait_for_locator(*locator)
        return self.selenium.find_element(*locator).text

    def get_attribute(attribute, *locator):
        '''Instance Method. Waits for locator, then gets the attribute.
        :Args:
        - attribute - for example, 'value', 'class' or 'style' 
        - locator - a tuple consisting of 
          * a constant from selenium.webdriver.common.by
          * a value
        '''
        self.wait_for_locator(*locator)
        return self.selenium.find_element(*locator).get_attribute(attribute)

    def clear_and_type(value, *locator):
        '''Instance Method. Waits for locator, sends keys, then waits for ajax to finish.
        :Args:
        - value - keys to send
        - locator - a tuple consisting of 
          * a constant from selenium.webdriver.common.by
          * a value
        '''
        self.wait_for_locator(*locator)
        element = self.selenium.find_element(*locator)
        element.clear()
        element.send_keys(value)
        self.wait_for_ajax()

    # XXX methods for checkboxes, radio buttons and select boxes?

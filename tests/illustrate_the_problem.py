import pytest

from selenium.webdriver.common.by import By

from JSAppPOM import JSAppPOM


class PageObject(object):

    def __init__(mozwebqa):
        self.mozwebqa = mozwebqa
        self.selenium = mozwebqa.selenium
        self.timeout = mozwebqa.timeout

    def ajax_has_stopped_now(self):
        return self.selenium.execute_script('return jQuery.active == 0')


class TestPlainPageObject(object):

    # click tests
    @pytest.mark.parametrize('element', ['button', 'link'])
    def test_click_does_not_wait_for_ajax_to_finish_before_returning(mozwebqa, element):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, element).click()
        assert not pom.ajax_has_stopped_now()

    @pytest.mark.parametrize('element', ['button', 'link'])
    def test_click_does_not_wait_for_element_to_be_visible(mozwebqa, element):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, element).click()
        try:
            pom.selenium.find_element(By.ID, 'second_' + element).click()
        except ElementNotVisibleException as e:
            asset e.msg == ""

    # send_keys tests
    def test_send_keys_does_not_wait_for_ajax_to_finish_before_returning(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        assert not pom.ajax_has_stopped_now()

    def test_send_keys_does_not_wait_for_element_to_be_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        try:
            pom.selenium.find_element(By.ID, 'second_text').send_keys('some other text\t')
        except ElementNotVisibleException as e:
            assert e.msg == ""

    # text tests
    def test_text_does_not_wait_for_element_to_be_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'link').click()
        try:
            pom.selenium.find_element(By.ID, 'second_link').text
        except ElementNotVisibleException as e:
            assert e.msg == ""

    # get_attribute tests
    def test_get_attribute_does_not_wait_for_element_to_be_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').click()
        try:
            pom.selenium.find_element(By.ID, 'second_text').get_attribute('value')
        except ElementNotVisibleException as e:
            assert e.msg == ""

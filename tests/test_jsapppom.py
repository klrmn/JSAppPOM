import pytest

from selenium.webdriver.common.by import By

from JSAppPOM import JSAppPOM


class TestJSAppPageObject(object):

    # click Tests
    @pytest.mark.parametrize('element', ['button', 'link'])
    def test_click_waits_for_element_visible_before_clicking(mozwebqa, element):
        pom = JSAppPOM(mozwebqa)
        # click first element the old way
        pom.selenium.find_element(By.ID, element).click()
        # second element will take 10 seconds to appear
        # click second element the new way
        pom.click(By.ID, 'second_' + element)
        # no ElementNotVisibleException

    @pytest.mark.parametrize('element', ['button', 'link'])
    def test_click_waits_for_ajax_to_finish_before_returning(mozwebqa, element):
        pom = JSAppPOM(mozwebqa)
        pom.click(By.ID, element)
        assert pom.ajax_has_stopped_now()

    @pytest.mark.parametrize('element', ['button', 'link'])
    def test_click_will_error_if_element_does_not_become_visible(mozwebqa, element):
        pom = PageObject(mozwebqa)
        try:
            pom.click(By.ID, 'third_' + element)
        except ElementNotVisibleException as e:
            assert e.msg == ""

    # send_keys tests
    def test_send_keys_waits_for_element_visible_before_typing(mozwebqa):
        pom = PageObject(mozwebqa)
        # type in the first elementt he old way
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        # second element will take 10 seconds to appear
        # type in second element the new way
        pom.send_keys('some new text', By.ID, 'second_text')
        # no ElementNotVisibleException

    def test_send_keys_waits_for_ajax_to_finish_before_returning(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.send_keys('some text\t', By.ID, 'text')
        assert pom.ajax_has_stopped_now()

    def test_send_keys_will_error_if_element_does_not_become_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        try:
            pom.send_keys('some text\t', By.ID, 'text')
        except ElementNotVisibleException as e:
            assert e.msg == ""
        
    # clear_and_type tests
    def test_clear_and_type_waits_for_element_visible_before_typing(mozwebqa):
        pom = PageObject(mozwebqa)
        # type in the first elementt he old way
        pom.selenium.find_element(By.ID, 'text').send_keys('some text\t')
        # second element will take 10 seconds to appear
        # type in second element the new way
        pom.clear_and_type('some new text', By.ID, 'second_text')
        # no ElementNotVisibleException

    def test_clear_and_type_waits_for_ajax_to_finish_before_returning(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.clear_and_type('some text\t', By.ID, 'text')
        assert pom.ajax_has_stopped_now()

    def test_clear_and_type_will_error_if_element_does_not_become_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        try:
            pom.clear_and_type('some text\t', By.ID, 'text')
        except ElementNotVisibleException as e:
            assert e.msg == ""

    # text tests
    def test_text_waits_for_element_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'link').click()
        # second span will take 10 seconds to appear
        assert pom.text(By.ID, 'second_link') == 'appearing'

    def test_text_errors_if_element_does_not_become_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        try:
            pom.text(By.ID, 'second_span')
        except ElementNotVisibleException as e:
            assert e.msg == ""

    # get_attribute tests
    def test_get_attribute_waits_for_element_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        pom.selenium.find_element(By.ID, 'text').click()
        assert pom.get_attribute('value', By.ID, 'second_text') == 'appearing'

    def test_get_attribute_if_element_does_not_become_visible(mozwebqa):
        pom = PageObject(mozwebqa)
        try:
            pom.get_attribute('value', By.ID, 'second_text')
        except ElementNotVisibleException as e:
            assert e.msg == ""


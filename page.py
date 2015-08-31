import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pytimeparse.timeparse import timeparse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RecordingsLocators, \
                     TrimLocators, \
                     LoginLocators, \
                     AdminLocators

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class LoginPage(BasePage):

    @property
    def username_input(self):
        return self.driver.find_element(*LoginLocators.USERNAME_INPUT)

    @property
    def password_input(self):
        return self.driver.find_element(*LoginLocators.PASSWORD_INPUT)

    @property
    def submit(self):
        return self.driver.find_element(*LoginLocators.SUBMIT_BUTTON)

    def login(self, username, password):
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.submit.click()

class AdminPage(BasePage):

    @property
    def recordings_tab(self):
        return self.driver.find_element(*AdminLocators.RECORDINGS_TAB)

class RecordingsPage(BasePage):

    @property
    def search_select(self):
        return Select(self.driver.find_element(*RecordingsLocators.SEARCH_SELECT))

    @property
    def search_input(self):
        return self.driver.find_element(*RecordingsLocators.SEARCH_INPUT)

    @property
    def per_page_select(self):
        return Select(self.driver.find_element(*RecordingsLocators.PERPAGE_SELECT))

    @property
    def refresh_checkbox(self):
        return self.driver.find_element(*RecordingsLocators.REFRESH_CHECKBOX)

    @property
    def on_hold_tab(self):
        return self.driver.find_element(*RecordingsLocators.ON_HOLD_TAB)

    @property
    def trim_iframe(self):
        return self.driver.find_element(*RecordingsLocators.TRIM_IFRAME)

    @property
    def trim_links(self):
        return self.driver.find_elements(*RecordingsLocators.TRIM_LINK)

    def refresh_off(self):
        if self.refresh_checkbox.is_selected():
            self.refresh_checkbox.click()

    def filter_recordings(self, field, value):
        self.search_select.select_by_value(field)
        self.search_input.send_keys(value)
        self.search_input.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(RecordingsLocators.FILTER_FOUND_COUNT)
        )

    def max_per_page(self):
        self.per_page_select.select_by_visible_text('100')


class TrimPage(BasePage):

    @property
    def trim_begin_input(self):
        return self.driver.find_element(*TrimLocators.CLIP_BEGIN_INPUT)

    @property
    def trim_end_input(self):
        return self.driver.find_element(*TrimLocators.CLIP_END_INPUT)

    @property
    def trim_ok_button(self):
        return self.driver.find_element(*TrimLocators.CLIP_OK_BUTTON)

    @property
    def split_remover(self):
        return self.driver.find_element(*TrimLocators.CLIP_REMOVE_BUTTON)

    @property
    def continue_button(self):
        return self.driver.find_element(*TrimLocators.CONTINUE_BUTTON)

    def trim(self):
        media_length = timeparse(self.trim_end_input.get_attribute('value'))
        trim_length = media_length / 10
        self.trim_begin_input.clear()
        self.trim_begin_input.send_keys(str(datetime.timedelta(seconds=trim_length)))
        self.trim_ok_button.click()
        self.split_remover.click()
        self.continue_button.click()

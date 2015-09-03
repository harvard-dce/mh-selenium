import datetime
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pytimeparse.timeparse import timeparse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    element_to_be_clickable as clickable, \
    presence_of_element_located as presence

from locators import RecordingsLocators, \
                                             UploadLocators, \
                                             TrimLocators, \
                                             LoginLocators, \
                                             AdminLocators

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def get_element(self, locator, condition=clickable):
        if condition is not None:
            return WebDriverWait(self.driver, 10).until(condition(locator))
        else:
            return self.driver.find_element(*locator)

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
        return self.get_element(AdminLocators.RECORDINGS_TAB)

    @property
    def upload_button(self):
        return self.get_element(AdminLocators.UPLOAD_BUTTON)

class RecordingsPage(BasePage):

    @property
    def search_select(self):
        return Select(self.get_element(RecordingsLocators.SEARCH_SELECT, clickable))

    @property
    def search_input(self):
        return self.get_element(RecordingsLocators.SEARCH_INPUT, clickable)

    @property
    def per_page_select(self):
        return Select(self.get_element(RecordingsLocators.PERPAGE_SELECT, clickable))

    @property
    def refresh_checkbox(self):
        return self.get_element(RecordingsLocators.REFRESH_CHECKBOX, clickable)

    @property
    def on_hold_tab(self):
        return self.get_element(RecordingsLocators.ON_HOLD_TAB, clickable)


    @property
    def trim_iframe(self):
        return self.get_element(RecordingsLocators.TRIM_IFRAME)

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
        found = self.get_element(RecordingsLocators.FILTER_FOUND_COUNT, presence)
        return found

    def max_per_page(self):
        self.per_page_select.select_by_visible_text('100')

    def switch_to_tab(self, tab_elem):
        """
        bypass the usual element click() method as these tab links frequently
        throw exceptions about not being clickable at point blah, blah
        """
        self.driver.execute_script("arguments[0].click();", tab_elem)


class UploadPage(BasePage):

    @property
    def title_input(self):
        return self.get_element(UploadLocators.TITLE_INPUT)

    @property
    def presenter_input(self):
        return self.get_element(UploadLocators.PRESENTER_INPUT)

    @property
    def course_input(self):
        return self.get_element(UploadLocators.COURSE_INPUT)

    @property
    def license_select(self):
        return Select(self.get_element(UploadLocators.LICENSE_SELECT))

    @property
    def rec_date_input(self):
        return self.get_element(UploadLocators.REC_DATE_INPUT)

    @property
    def start_hour_select(self):
        return Select(self.get_element(UploadLocators.START_HOUR_SELECT))

    @property
    def start_minute_select(self):
        return Select(self.get_element(UploadLocators.START_MINUTE_SELECT))

    @property
    def contributor_input(self):
        return self.get_element(UploadLocators.CONTRIBUTOR_INPUT)

    @property
    def type_input(self):
        return self.get_element(UploadLocators.TYPE_INPUT)

    @property
    def subject_input(self):
        return self.get_element(UploadLocators.SUBJECT_INPUT)

    @property
    def lang_input(self):
        return self.get_element(UploadLocators.LANG_INPUT)

    @property
    def desc_input(self):
        return self.get_element(UploadLocators.DESC_INPUT)

    @property
    def copyright_input(self):
        return self.get_element(UploadLocators.COPYRIGHT_INPUT)

    @property
    def single_upload_radio(self):
        return self.get_element(UploadLocators.SINGLE_UPLOAD_RADIO)

    @property
    def multi_upload_radio(self):
        return self.get_element(UploadLocators.MULTI_UPLOAD_RADIO)

    @property
    def local_file_radio(self):
        return self.get_element(UploadLocators.LOCAL_FILE_RADIO)

    @property
    def inbox_file_radio(self):
        return self.get_element(UploadLocators.INBOX_FILE_RADIO)

    @property
    def local_file_upload_iframe(self):
        iframes = self.driver.find_elements(*UploadLocators.FILE_UPLOAD_IFRAME)
        # should be the first one, but ugh.
        return iframes[0]

    @property
    def local_file_selector(self):
        return self.get_element(UploadLocators.LOCAL_FILE_SELECTOR)

    @property
    def inbox_file_select(self):
        return Select(self.get_element(UploadLocators.INBOX_FILE_SELECT))

    @property
    def contains_slides_checkbox(self):
        return self.get_element(UploadLocators.CONTAINS_SLIDES_CHECKBOX)

    @property
    def workflow_select(self):
        return Select(self.get_element(UploadLocators.WORKFLOW_SELECT))

    @property
    def live_stream_checkbox(self):
        return self.get_element(UploadLocators.LIVE_STREAM_CHECKBOX)

    @property
    def multitrack_checkbox(self):
        return self.get_element(UploadLocators.MULTITRACK_CHECKBOX)

    @property
    def upload_button(self):
        return self.get_element(UploadLocators.UPLOAD_BUTTON)

    def set_file_upload(self, file_path):
        self.single_upload_radio.click()
        self.local_file_radio.click()
        self.driver.switch_to.frame(self.local_file_upload_iframe)
        self.local_file_selector.send_keys(file_path)
        self.driver.switch_to.default_content()

class TrimPage(BasePage):

    @property
    def trim_begin_input(self):
        return self.get_element(TrimLocators.CLIP_BEGIN_INPUT)

    @property
    def trim_end_input(self):
        return self.get_element(TrimLocators.CLIP_END_INPUT)

    @property
    def trim_ok_button(self):
        return self.get_element(TrimLocators.CLIP_OK_BUTTON)

    @property
    def split_remover(self):
        return self.get_element(TrimLocators.CLIP_REMOVE_BUTTON)

    @property
    def continue_button(self):
        return self.get_element(TrimLocators.CONTINUE_BUTTON)

    def trim(self):
        media_length = timeparse(self.trim_end_input.get_attribute('value'))
        trim_length = media_length / 10
        self.trim_begin_input.clear()
        self.trim_begin_input.send_keys(str(datetime.timedelta(seconds=trim_length)))
        self.trim_ok_button.click()
        self.split_remover.click()
        self.continue_button.click()
        sleep(2)

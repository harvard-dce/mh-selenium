
from selenium.webdriver.common.by import By

class LoginLocators(object):
    USERNAME_INPUT = (By.NAME, 'j_username')
    PASSWORD_INPUT = (By.NAME, 'j_password')
    SUBMIT_BUTTON = (By.NAME, 'submit')

class AdminLocators(object):
    RECORDINGS_TAB = (By.CSS_SELECTOR, 'a#i18n_tab_recording')

class RecordingsLocators(object):
    SEARCH_SELECT = (By.CSS_SELECTOR, 'div#searchBox > select')
    SEARCH_INPUT = (By.CSS_SELECTOR, 'div#searchBox > span > input')
    PERPAGE_SELECT = (By.CSS_SELECTOR, 'select#pageSize')
    REFRESH_CHECKBOX = (By.CSS_SELECTOR, 'input#refreshEnabled')
    TRIM_LINK = (By.XPATH, '//a[@title="Review / VideoEdit"]')
    TRIM_IFRAME = (By.CSS_SELECTOR, 'iframe#holdActionUI')

class TrimLocators(object):
    CLIP_BEGIN_INPUT = (By.CSS_SELECTOR, 'span#clipBegin > input')
    CLIP_END_INPUT = (By.CSS_SELECTOR, 'span#clipEnd > input')
    CLIP_OK_BUTTON = (By.CSS_SELECTOR, 'input#okButton')
    CLIP_REMOVE_BUTTON = (By.CSS_SELECTOR, 'a#splitRemover-0')
    CONTINUE_BUTTON = (By.CSS_SELECTOR, 'input#continueButton')


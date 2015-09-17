
import pytest

from mh_selenium.pages import AdminPage, LoginPage

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox",
                     help="Selenium webdriver to use")
    parser.addoption("--base_url", action="store",
                     help="Matterhorn admin base url")
    parser.addoption("--admin_username", action="store",
                     help="Matterhorn admin username")
    parser.addoption("--admin_password", action="store",
        help="Matterhorn admin password")

@pytest.fixture(scope='session')
def splinter_make_screenshot_on_failure():
    return False

@pytest.fixture(scope='session')
def splinter_webdriver(request):
    """Override splinter webdriver name."""
    return request.config.getoption("--browser")

@pytest.fixture
def admin_page(browser, base_url):
    browser.visit(base_url + '/admin')
    return AdminPage(browser)

@pytest.fixture
def login_page(browser, base_url):
    browser.visit(base_url + '/login.html')
    return LoginPage(browser)

@pytest.fixture
def admin_username(request):
    return request.config.getoption("--admin_username")

@pytest.fixture
def admin_password(request):
    return request.config.getoption("--admin_password")

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base_url")

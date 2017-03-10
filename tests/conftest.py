
import pytest
import pyhorn
from mh_pages import pages

def pytest_addoption(parser):
    parser.addoption('--admin_pass', dest='admin_pass', action='store')
    parser.addoption('--admin_user', dest='admin_user', action='store')
    parser.addoption('--api_pass', dest='api_pass', action='store')
    parser.addoption('--api_user', dest='api_user', action='store')
    parser.addoption('--mpid', dest='mpid', action='store')
    parser.addoption('-D', dest='driver', action='store', default='chrome')
    parser.addoption('-H', dest='host', action='store')

def pytest_configure(config):
    for opt in ('host', 'admin_user', 'admin_pass', 'api_user', 'api_pass'):
        if getattr(config.option, opt) is None:
            raise pytest.UsageError("missing %s option" % opt)

@pytest.fixture(scope='session')
def splinter_make_screenshot_on_failure():
    return False

@pytest.fixture
def opt_getter(request):
    def func(opt, default=None):
        return getattr(request.config.option, opt, default)
    return func

@pytest.fixture
def splinter_webdriver(opt_getter):
    return opt_getter('driver')

@pytest.fixture
def admin_browser(opt_getter, request, browser_instance_getter):

    host = opt_getter('host')
    admin_user = opt_getter('admin_user')
    admin_pass = opt_getter('admin_pass')

    browser = browser_instance_getter(request, admin_browser)
    browser.visit(host)
    if 'Login' in browser.title:
        page = pages.LoginPage(browser)
        with page.wait_for_page_change():
            page.login(admin_user, admin_pass)
            if 'Login' in browser.title:
                raise RuntimeError(
                    "Login failed. Check your user/pass.")
    return browser

@pytest.fixture
def engage_browser(admin_browser):
    page = pages.WelcomePage(admin_browser)
    page.engage_link.click()
    return page.browser

@pytest.fixture
def player(opt_getter, request, browser_instance_getter):
    host = opt_getter('host')
    mpid = opt_getter('mpid')
    player_url = host + '/engage/player/watch.html?id=' + mpid
    browser = browser_instance_getter(request, player)
    browser.visit(player_url)
    return browser

@pytest.fixture
def mh_api(opt_getter):
    host = opt_getter('host')
    api_user = opt_getter('api_user')
    api_pass = opt_getter('api_pass')


import pytest
from os import getenv

import pyhorn
from mh_pages import pages


def pytest_addoption(parser):
    parser.addoption('--admin_pass', dest='admin_pass', action='store')
    parser.addoption('--admin_user', dest='admin_user', action='store')
    parser.addoption('--rest_pass', dest='rest_pass', action='store')
    parser.addoption('--rest_user', dest='rest_user', action='store')
    parser.addoption('--admin_host', dest='admin_host', action='store')
    parser.addoption('--engage_host', dest='engage_host', action='store')
    parser.addoption('--user_agent', dest='user_agent', action='store')
    parser.addoption('-D', dest='driver', action='store', default='chrome')

    parser.addoption('--mpid', dest='mpid', action='store')

def pytest_configure(config):
    def set_default_from_env(opt, envvar):
        if getattr(config.option, opt) is None:
            setattr(config.option, opt, getenv(envvar))
    set_default_from_env('admin_host', 'MHUIT_ADMIN_HOST')
    set_default_from_env('engage_host', 'MHUIT_ENGAGE_HOST')
    set_default_from_env('admin_user', 'MHUIT_ADMIN_USER')
    set_default_from_env('admin_pass', 'MHUIT_ADMIN_PASS')
    set_default_from_env('rest_user', 'MHUIT_REST_USER')
    set_default_from_env('rest_pass', 'MHUIT_REST_PASS')
    set_default_from_env('user_agent', 'MHUIT_USER_AGENT')

@pytest.fixture(scope='session')
def splinter_make_screenshot_on_failure():
    return False

@pytest.fixture(scope='session')
def opt_getter(request):
    def func(opt, default=None):
        return getattr(request.config.option, opt, default)
    return func

@pytest.fixture(scope='session')
def splinter_webdriver(opt_getter):
    return opt_getter('driver')

@pytest.fixture(scope='session')
def splinter_driver_kwargs(opt_getter):
    kwargs = {}
    user_agent = opt_getter('user_agent')
    if user_agent is not None:
        kwargs['user_agent'] = user_agent
    return kwargs

@pytest.fixture
def admin_browser(opt_getter, request, browser_instance_getter):

    admin_host = opt_getter('admin_host')
    admin_user = opt_getter('admin_user')
    admin_pass = opt_getter('admin_pass')

    browser = browser_instance_getter(request, admin_browser)
    browser.visit(admin_host)
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

@pytest.fixture(scope='session')
def player_getter(opt_getter, request, browser_instance_getter):
    host = opt_getter('engage_host')
    def get_player(mpid):
        print host, mpid
        player_url = host + '/engage/player/watch.html?id=' + mpid
        browser = browser_instance_getter(request, player_getter)
        browser.visit(player_url)
        return browser
    return get_player

@pytest.fixture(scope='session')
def api_instance_getter(opt_getter):
    rest_user = opt_getter('rest_user')
    rest_pass = opt_getter('rest_pass')
    def get_api(host_opt):
        host = opt_getter(host_opt)
        return pyhorn.MHClient(host, rest_user, rest_pass,
                               timeout=30, cache_enabled=False)
    return get_api

@pytest.fixture
def admin_api(api_instance_getter):
    return api_instance_getter('admin_host')

@pytest.fixture
def engage_api(api_instance_getter):
    return api_instance_getter('engage_host')


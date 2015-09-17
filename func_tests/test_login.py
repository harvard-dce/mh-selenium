from hamcrest import *

def test_redirect_to_login(browser, base_url):
    browser.visit(base_url + '/admin')
    assert_that(browser.title, contains_string('Login Page'))

def test_successful_login(browser, login_page, admin_username, admin_password):
    with login_page.wait_for_page_unload():
        login_page.login(admin_username, admin_password)
    assert_that(browser.url, ends_with('welcome.html'))

def test_failed_login(browser, login_page):
    with login_page.wait_for_page_unload():
        login_page.login('foo','bar')
    assert_that(browser.url, ends_with('login.html?error'))

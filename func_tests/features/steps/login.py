from behave import given, when, then
from hamcrest import *
from mh_selenium.pages import LoginPage

@given('we visit the admin site')
def impl(context):
    context.browser.visit(context.base_url + '/admin')

@given('we are on the login page')
def impl(context):
    context.browser.visit(context.base_url + '/login.html')

@then('we are redirected to the login page')
def impl(context):
    assert_that(context.browser.title, contains_string('Login Page'))

@when('we provide correct credentials')
def impl(context):
    page = LoginPage(context.browser.driver)
    page.login(context.admin_username, context.admin_password)

@then('we see the recordings page')
def impl(context):
    assert_that(context.browser.url, ends_with('#/recordings'))

@when('we provide incorrect credentials')
def impl(context):
    page = LoginPage(context.browser.driver)
    page.login('foo', 'bar')

@then('we see a login error')
def impl(context):
    assert_that(context.browser.url, ends_with('login.html?error'))

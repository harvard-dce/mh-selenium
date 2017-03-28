
def test_admin_login_fixture(admin_browser):
    assert 'Release' in admin_browser.title


def test_admin_login(browser, opt_getter):

    # get the login deets
    admin_host = opt_getter('admin_host')
    admin_user = opt_getter('admin_user')
    admin_pass = opt_getter('admin_pass')

    # go to the admin site
    browser.visit(admin_host)

    # fill in the user/pass
    browser.fill('j_username', admin_user)
    browser.fill('j_password', admin_pass)

    # click submit
    browser.find_by_name('submit').click()

    assert 'Release' in browser.title
    return

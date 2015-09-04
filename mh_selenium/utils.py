import click
from functools import wraps
from urlparse import urljoin
from selenium import webdriver
from mh_selenium.pages import LoginPage

class ClickState(object):

    def __init__(self):
        self.username = None
        self.password = None
        self.base_url = None
        self.driver = None


pass_state = click.make_pass_decorator(ClickState, ensure=True)

def common_callback(ctx, option, value):
    state = ctx.ensure_object(ClickState)
    setattr(state, option.name, value)
    return value

def password_option(f):
    return click.option('-p','--password',
                        expose_value=False,
                        prompt=True,
                        callback=common_callback)(f)

def username_option(f):
    return click.option('-u','--username',
                        expose_value=False,
                        prompt=True,
                        callback=common_callback)(f)

def base_url_arg(f):
    return click.argument('base_url',
                          expose_value=False,
                          callback=common_callback)(f)

def common_options(f):
    f = password_option(f)
    f = username_option(f)
    f = base_url_arg(f)
    return f

def init_driver(init_path=''):
    def decorator(click_cmd):
        @wraps(click_cmd)
        def _wrapped_cmd(state, *args, **kwargs):

            state.driver = webdriver.Firefox()
            state.driver.implicitly_wait(10)
            state.driver.get(urljoin(state.base_url, init_path))

            if 'Login' in state.driver.title:
                page = LoginPage(state.driver)
                page.login(state.username, state.password)

            result = click_cmd(state, *args, **kwargs)

            state.driver.close()
            state.driver.quit()

            return result

        return _wrapped_cmd
    return decorator

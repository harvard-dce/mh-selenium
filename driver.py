
from selenium import webdriver
from time import sleep
from urlparse import urljoin

import click
click.disable_unicode_literals_warning = True

from page import RecordingsPage, LoginPage, AdminPage, TrimPage

@click.group()
def cli():
    pass

@cli.command()
@click.argument('base_url')
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True)
@click.option('-f', '--filter')
@click.option('-c', '--count', type=int)
def run_trims(base_url, username, password, filter=None, count=None):

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(urljoin(base_url, '/admin'))

    if 'Login' in driver.title:
        login_page = LoginPage(driver)
        login_page.login(username, password)
        sleep(1)

    recs_page = RecordingsPage(driver)
    recs_page.refresh_off()
    recs_page.max_per_page()
    recs_page.on_hold_tab.click()
    sleep(1)

    if filter is not None:
        field, value = filter.split(':', 1)
        recs_page.filter_recordings(field, value)
        sleep(1)

    js_links = [x.get_attribute('href') for x in recs_page.trim_links]

    if count is not None:
        js_links = js_links[:count]

    for js_link in js_links:
        scheme, js = js_link.split(':', 1)
        driver.execute_script(js)
        driver.switch_to.frame(recs_page.trim_iframe)
        sleep(1)
        trim_page = TrimPage(driver)
        trim_page.trim()
        driver.switch_to.default_content()

    driver.close()
    driver.quit()

if __name__ == '__main__':
    cli()

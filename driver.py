
from selenium import webdriver
from time import sleep
from urlparse import urljoin

import click
click.disable_unicode_literals_warning = True

from mh_selenium.pages import RecordingsPage, LoginPage, AdminPage, TrimPage

@click.group()
def cli():
    pass

@cli.command()
@click.argument('base_url')
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True)
@click.option('-f', '--filter')
@click.option('-c', '--count', type=int, default=None)
def run_trims(base_url, username, password, filter=None, count=None):

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(urljoin(base_url, '/admin'))

    if 'Login' in driver.title:
        page = LoginPage(driver)
        page.login(username, password)

    page = RecordingsPage(driver)
    page.max_per_page()
    page.on_hold_tab.click()
    page.refresh_off()

    if filter is not None:
        field, value = filter.split(':', 1)
        page.filter_recordings(field, value)

    for link in page.trim_links[:count]:
        href = link.get_attribute('href')
        scheme, js = href.split(':', 1)
        driver.execute_script(js)
        driver.switch_to.frame(page.trim_iframe)
        sleep(1)
        page = TrimPage(driver)
        page.trim()
        driver.switch_to.default_content()

    driver.close()
    driver.quit()

if __name__ == '__main__':
    cli()

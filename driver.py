
from selenium import webdriver
from time import sleep
from urlparse import urljoin

import click
click.disable_unicode_literals_warning = True

from mh_selenium.pages import RecordingsPage, LoginPage, AdminPage, TrimPage, \
                              UploadPage

@click.group()
def cli():
    pass

@cli.command()
@click.argument('base_url')
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True)
@click.option('-f', '--file')
def upload(base_url, username, password, file):

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(urljoin(base_url, '/admin'))

    if 'Login' in driver.title:
        page = LoginPage(driver)
        page.login(username, password)

    page = AdminPage(driver)
    page.upload_button.click()

    page = UploadPage(driver)
    page.title_input.send_keys("My Test Upload")
    page.type_input.send_keys("L01")
    page.set_file_upload(file)
    page.workflow_select.select_by_value('DCE-production')
    page.live_stream_checkbox.click()
    page.multitrack_checkbox.click()
    page.upload_button.click()

    driver.close()
    driver.quit()

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
    page.switch_to_tab(page.on_hold_tab)
    page.refresh_off()

    if filter is not None:
        field, value = filter.split(':', 1)
        page.filter_recordings(field, value)

    for link in page.trim_links[:count]:
        href = link.get_attribute('href')
        scheme, js = href.split(':', 1)
        driver.execute_script(js)
        driver.switch_to.frame(page.trim_iframe)
        page = TrimPage(driver)
        page.trim()
        driver.switch_to.default_content()

    driver.close()
    driver.quit()

if __name__ == '__main__':
    cli()

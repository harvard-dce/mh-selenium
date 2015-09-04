
import click
click.disable_unicode_literals_warning = True

from mh_selenium.utils import common_options, pass_state, init_driver
from mh_selenium.pages import RecordingsPage, AdminPage, TrimPage, \
                              UploadPage

@click.group()
def cli():
    pass

@cli.command()
@click.option('-f', '--file')
@common_options
@pass_state
@init_driver('/admin')
def upload(state, file):

    page = AdminPage(state.driver)
    page.upload_button.click()

    page = UploadPage(state.driver)
    page.title_input.send_keys("My Test Upload")
    page.type_input.send_keys("L01")
    page.set_file_upload(file)
    page.workflow_select.select_by_value('DCE-production')
    page.live_stream_checkbox.click()
    page.multitrack_checkbox.click()
    page.upload_button.click()

@cli.command()
@click.option('-f', '--filter')
@click.option('-c', '--count', type=int, default=None)
@common_options
@pass_state
@init_driver('/admin')
def trim(state, filter=None, count=None):

    page = RecordingsPage(state.driver)
    page.max_per_page()
    page.switch_to_tab(page.on_hold_tab)
    page.refresh_off()

    if filter is not None:
        field, value = filter.split(':', 1)
        page.filter_recordings(field, value)

    for link in page.trim_links[:count]:
        href = link.get_attribute('href')
        scheme, js = href.split(':', 1)
        state.driver.execute_script(js)
        state.driver.switch_to.frame(page.trim_iframe)
        page = TrimPage(state.driver)
        page.trim()
        state.driver.switch_to.default_content()

if __name__ == '__main__':
    cli()

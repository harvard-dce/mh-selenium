#!/usr/bin/env python
from time import sleep

import click
from fabric.context_managers import cd

click.disable_unicode_literals_warning = True

from unipath import Path
from fabric.api import run, abort, env, hide, sudo
from fabric.operations import put
from fabric.colors import cyan
from fabric.contrib.files import exists as remote_exists

from mh_selenium.utils import selenium_options, inbox_options, pass_state, \
    init_driver, base_url_arg, init_fabric
from mh_selenium.pages import RecordingsPage, AdminPage, TrimPage, \
                              UploadPage

@click.group()
def cli():
    pass

@cli.command()
@click.option('--presenter')
@click.option('--presentation')
@click.option('--combined')
@click.option('-i', '--inbox', is_flag=True)
@click.option('--live_stream', is_flag=True)
@selenium_options
@pass_state
@init_driver('/admin')
def upload(state, presenter, presentation, combined, inbox, live_stream):

    page = AdminPage(state.driver)
    page.upload_button.click()

    page = UploadPage(state.driver)
    page.title_input.send_keys("My Test Upload")
    page.type_input.send_keys("L01")
    page.set_upload_files(presenter=presenter,
                          presentation=presentation,
                          combined=combined,
                          is_inbox=inbox)
    page.workflow_select.select_by_value('DCE-production')
    page.set_live_stream(live_stream)
    page.set_multitrack(combined is not None)
    page.upload_button.click()
    page.wait_for_upload_finish()

@cli.command()
@click.option('-f', '--filter')
@click.option('-c', '--count', type=int, default=None)
@selenium_options
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

@cli.group()
@pass_state
def inbox(state):
    pass

@inbox.command(name='put')
@click.option('-f', '--file')
@inbox_options
@pass_state
@init_fabric
def inbox_put(state, file):
    result = put(local_path=file, remote_path=state.inbox_path, use_sudo=True)
    print(cyan("Files created: {}".format(str(result))))

@inbox.command(name='symlink')
@click.option('-f', '--file')
@click.option('-c', '--count', type=int, default=1)
@inbox_options
@pass_state
@init_fabric
def inbox_symlink(state, file, count):

    remote_path = state.inbox_dest.child(file)
    if not remote_exists(remote_path, verbose=True):
        abort("remote file {} not found".format(remote_path))

    with cd(state.inbox_path):
        for i in range(count):
            link = remote_path.stem + '_' + str(i) + remote_path.ext
            sudo("ln -s {} {}".format(remote_path, link))
        return

@inbox.command(name='list')
@click.argument('match', default='')
@inbox_options
@pass_state
@init_fabric
def inbox_list(state, match):
    with cd(state.inbox_dest), hide('running', 'stdout', 'stderr'):
        output = run('ls {}'.format(match))
        for f in output.split():
            print(cyan(f))


if __name__ == '__main__':
    cli()

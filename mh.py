#!/usr/bin/env python
from time import sleep

import click
from click.exceptions import UsageError
from fabric.context_managers import cd
from selenium.common.exceptions import TimeoutException

click.disable_unicode_literals_warning = True

from os.path import basename, exists, getsize, dirname
from fabric.api import run, abort, hide, sudo, local, lcd
from fabric.operations import put
from fabric.colors import cyan
from fabric.contrib.files import exists as remote_exists

from mh_cli.cli import selenium_options, \
                       inbox_options, \
                       ClickState, \
                       init_driver, \
                       init_fabric

from mh_pages.pages import RecordingsPage, \
                           AdminPage, \
                           TrimPage, \
                           UploadPage

pass_state = click.make_pass_decorator(ClickState, ensure=True)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--presenter')
@click.option('--presentation')
@click.option('--combined')
@click.option('--title', default='mh-selenium upload')
@click.option('-i', '--inbox', is_flag=True)
@click.option('--live_stream', is_flag=True)
@selenium_options
@pass_state
@init_driver('/admin')
def upload(state, presenter, presentation, combined, title, inbox, live_stream):
    """Execute an automated recording upload"""

    page = RecordingsPage(state.driver)
    page.upload_recording_button.click()

    page = UploadPage(state.driver)

    page.enter_text(page.title_input, title)
    page.enter_text(page.type_input, "L01")
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
    """Execute a trim operation on existing recording(s)"""

    page = AdminPage(state.driver)
    page.recordings_tab.click()
    page = RecordingsPage(state.driver)
    page.max_per_page()
    page.switch_to_tab(page.on_hold_tab)

    if filter is not None:
        field, value = filter.split(':', 1)
        page.filter_recordings(field, value)

    link_idx = 0
    while True:

        # kinda annoying that we have to do this each time
        page.refresh_off()

        try:
            # re-resolve the trim link elements each time because the refs go
            # stale when the page reloads
            # also, iterate via incrementing idx so that we don't somehow trim
            # the same thing > once (e.g. the entry doesn't get removed from
            # the table because the workflow hasn't actually resumed)
            link = page.trim_links[link_idx]
        except (TimeoutException,IndexError):
            break

        href = link.get_attribute('href')
        scheme, js = href.split(':', 1)
        page.js(js)
        page.switch_frame(page.trim_iframe)
        page = TrimPage(state.driver)
        page.trim()
        page.default_frame()
        page.reload()
        page = RecordingsPage(state.driver)

        if count is not None:
            count -= 1
            if count == 0:
                break


@cli.group()
def gi():
    """Do stuff with Ghost Inspector tests"""


@gi.command(name='list', context_settings=dict(ignore_unknown_options=True))
@click.argument('gi_args', nargs=-1, type=click.UNPROCESSED)
def gi_list(gi_args):
    """Collect and list available tests"""
    with(lcd(dirname(__file__))):
        local("py.test --verbose --collect-only %s" % " ".join(gi_args))


@gi.command(name='exec', context_settings=dict(ignore_unknown_options=True))
@click.argument('gi_args', nargs=-1, type=click.UNPROCESSED)
def gi_exec(gi_args):
    """Execute tests"""
    with(lcd(dirname(__file__))):
        local("py.test --verbose %s" % " ".join(gi_args))


@cli.group()
def inbox():
    """Manipulate the MH recording file inbox"""

@inbox.command(name='put')
@click.option('-f', '--file')
@inbox_options
@pass_state
@init_fabric
def inbox_put(state, file):
    """Upload a recording file to the MH inbox"""
    if file.startswith('http'):
        with cd(state.inbox):
            sudo("curl -s -o %s %s" % (basename(file), file))
        result = state.inbox + '/' + basename(file)
    elif exists(file):
        size_in_bytes = getsize(file)
        if size_in_bytes / (1024 * 1024) > 1024:
            raise UsageError("File > 1G. Upload to s3 and use the url instead.")
        result = put(local_path=file, remote_path=state.inbox, use_sudo=True)
    else:
        raise UsageError("Local file %s not found" % file)
    print(cyan("Files created: {}".format(str(result))))

@inbox.command(name='symlink')
@click.option('-f', '--file')
@click.option('-c', '--count', type=int, default=1)
@inbox_options
@pass_state
@init_fabric
def inbox_symlink(state, file, count):
    """Create copies of an existing inbox file via symlinks"""
    remote_path = state.inbox_dest.child(file)
    if not remote_exists(remote_path, verbose=True):
        abort("remote file {} not found".format(remote_path))

    with cd(state.inbox):
        for i in range(count):
            link = remote_path.stem + '_' + str(i + 1) + remote_path.ext
            sudo("ln -s {} {}".format(remote_path, link))
        return

@inbox.command(name='list')
@click.argument('match', default='')
@inbox_options
@pass_state
@init_fabric
def inbox_list(state, match):
    """List the current contents of the inbox"""
    if not remote_exists(state.inbox_dest):
        return
    with cd(state.inbox_dest), hide('running', 'stdout', 'stderr'):
        output = run('ls {}'.format(match))
        for f in output.split():
            print(cyan(f))


if __name__ == '__main__':
    cli()

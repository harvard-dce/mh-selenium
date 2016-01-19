__version__ = '0.8.0'

import click
click.disable_unicode_literals_warning = True

@click.group()
def cli():
    pass

from gi import gi
from inbox import inbox
from rec import rec
from series import series

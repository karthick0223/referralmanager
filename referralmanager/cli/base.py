import logging
import click
import json
import os
import pdb
import sys

from .dbimport import dbimport as dbimport_cmd
from .fetch import fetch as fetch_cmd
import raven

print('Welcome......')
@click.group()
@click.option('--sentry-login', type=str, default=os.path.expanduser("~/.sentrylogin"),
              help="Location of file with sentry user and project details.")
@click.option('--loglevel', default='INFO', help='level of logging')
@click.pass_context
def base(ctx, sentry_login, loglevel):
    with open(sentry_login) as f:
        sentry_access_details = json.load(f)
        public_key = sentry_access_details["public_key"]
        secret = sentry_access_details["secret"]
        project = sentry_access_details["project"]

    sentry_client = raven.Client('https://{}:{}@app.getsentry.com/{}'.format(public_key, secret, project))
    ctx.obj = sentry_client
    setup_logging(loglevel)


def setup_logging(loglevel="INFO"):
    """
    Set up logging
    :param loglevel: loglevel to use, one of ERROR, WARNING, DEBUG, INFO (default INFO)
    :return:
    """
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level,
                        format='%(levelname)s %(asctime)s %(funcName)s - %(message)s')
    logging.debug("Started log with loglevel %(loglevel)s" % {"loglevel": loglevel})


base.add_command(dbimport_cmd)
base.add_command(fetch_cmd)

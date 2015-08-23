from argparse import ArgumentParser
import sys
from six.moves.configparser import ConfigParser

from grabctl.web import run_web_daemon

DEFAULT_CONFIG = {
    'host': 'localhost', 
    'port': 7777,
    'debug': False,
    'database': 'var/grabctl.json',
}

USAGE = 'Usage: grabctl <command> [opts]'


def command_daemon(config):
    host = config.get('grabctl', 'host')
    port = config.getint('grabctl', 'port')
    debug = config.getboolean('grabctl', 'debug')
    database = config.get('grabctl', 'database')
    run_web_daemon(host=host, port=port, debug=debug, database=database)


def run():
    config = ConfigParser(DEFAULT_CONFIG)
    config.read('grabctl.ini')

    cli_parser = ArgumentParser(usage=USAGE)
    cli_parser.add_argument('command')
    opts = cli_parser.parse_args()
    if opts.command == 'daemon':
        command_daemon(config)
    else:
        sys.stderr.write('Unknown command: %s\n' % opts.command)
        sys.stderr.write(USAGE + '\n')
        sys.exit(1)

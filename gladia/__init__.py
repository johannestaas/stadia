'''
gladia

Let the gladiator games begin!
'''

__title__ = 'gladia'
__version__ = '0.0.1'
__all__ = ()
__author__ = 'Johan Nestaas <johannestaas@gmail.com'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2020 Johan Nestaas'


from .game import start
from .log import setup_logging
from .debug import debug_fight


def main():
    import argparse
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', '-d', default=None,
        help='run tests',
    )
    args = parser.parse_args()
    if args.debug is None:
        start()
    elif args.debug == 'fight':
        debug_fight()

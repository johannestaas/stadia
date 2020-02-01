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


def main():
    setup_logging()
    start()

"""
Tools to log to screen, rolling files, and logger server.
"""

import logging
import logging.handlers
import os
import errno
import sys
import json
import itertools
import re
import inspect
from .tools import pairwise
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s')

def setup(**args):
    destinations = args['to']
    if isinstance(destinations, basestring):
        destinations = [destinations]
    try:
        outer_frame = inspect.stack()[1][0]
        mod_name = args.get('module', outer_frame.f_globals['__name__'])
        filename = args.get('filename', '{}.log'.format(mod_name))
        directory = args.get('directory', '/tmp')
        logger = logging.getLogger(mod_name)
        for dest in destinations:
            if dest == 'file':
                handler = logging.handlers.RotatingFileHandler(
                    os.path.join(directory, filename))
            if dest == 'console':
                handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    finally:
        del outer_frame
        


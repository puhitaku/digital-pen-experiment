# -*- coding: utf-8 -*-
"""Digital Pen Experiment (Educator Support Tool w/ Digital Pen)

"""

import sys
from PluginManager import DpxPluginManager
from Logger import Logger

def main():
    log = Logger('main').get_logger_object()
    log.debug('Welcome')

    manager = DpxPluginManager()



if __name__ == '__main__':
    main()
    sys.exit()
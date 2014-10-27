#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from cli.main import Cli_Main
from core.mehilaismanageri import Mehilaismanageri

if __name__ == "__main__":
    '''
    Starts application.
    '''
    argv1 = None
    mehilaismanageri = Mehilaismanageri()
    
    if len(sys.argv) > 1:
        argv1 = sys.argv[1]
    
    if argv1 == "gui":
        print "no graphical user interface"
    else:
        ui = Cli_Main(mehilaismanageri, sys.argv)
        ui.start()


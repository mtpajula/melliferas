#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class Cli_Template(object):
    
    def __init__(self):
        
        self.title = "Template"
        self.level = 0
        self.commands = {
                    "lopeta" : self.exit_system,
                    "komennot" : self.print_commands
                    }
                    
    def add_level(self):
        self.level += 1
        
    def start(self):
        
        while (True):
            
            syote = raw_input("[ " + str(self.level) + " ]: ")
            
            if syote in self.commands:
                
                if self.commands[syote] is None:
                    break
                else:
                    self.commands[syote]()
            else:
                print "\n ! tuntematon komento"
    
    def exit_system(self):
        sys.exit()
    
    def print_commands(self):
        print "\n == " + self.title + ". Komennot ==> "
        first = False
        for s in self.commands:
            if first is True:
                print ", ",
            print s,
            first = True
            
        print ""
        

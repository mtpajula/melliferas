#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import fnmatch
import csv
from csv_reader import Csv_Reader

class Dataluku(object):
    
    def __init__(self, settings, messages, mehilaispesa):
        
        self.messages = messages
        self.settings = settings
        self.mehilaispesa = mehilaispesa
        
        self.reader = Csv_Reader(self.messages)
    
    def load(self, datafolder = None):
        
        if datafolder is None:
            datafolder = self.settings.d["datafolder"]
        
        self.messages.add("Luetaan kansiosta " + datafolder, "Dataluku")
        
        for root, dirs, files in os.walk(datafolder):
            for filename in fnmatch.filter(files, self.settings.d["filetype_pattern"]):
                
                self.reader.load(os.path.join(root, filename), self.mehilaispesa)

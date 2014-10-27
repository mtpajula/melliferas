#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import fnmatch
import csv
from csv_data_reader import Csv_Data_Reader
from csv_plate_reader import Csv_Plate_Reader

class Dataluku(object):
    
    def __init__(self, settings, messages, mehilaispesa):
        
        self.messages = messages
        self.settings = settings
        self.mehilaispesa = mehilaispesa
        
        self.data_reader = Csv_Data_Reader(self.messages)
        self.plate_reader = Csv_Plate_Reader(self.messages)
    
    def load_plates(self, datafolder = None):
        self.read(self.plate_reader, datafolder)
        
    def read(self, reader, datafolder):
        if datafolder is None:
            datafolder = self.settings.d["datafolder"]
        
        self.messages.add("Luetaan kansiosta " + datafolder, "Dataluku")
        
        for root, dirs, files in os.walk(datafolder):
            for filename in fnmatch.filter(files, self.settings.d["data_filetype_pattern"]):
                
                reader.load(os.path.join(root, filename), self.mehilaispesa)
        

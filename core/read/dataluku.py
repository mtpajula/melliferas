#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import fnmatch
import csv
from csv_data_reader import Csv_Data_Reader
from csv_plate_reader import Csv_Plate_Reader

class Dataluku(object):
    
    def __init__(self, settings, messages, mehilaispesa, datahallinta):
        
        self.messages = messages
        self.settings = settings
        self.mehilaispesa = mehilaispesa
        self.datahallinta = datahallinta
        
        self.data_reader = Csv_Data_Reader(self.messages)
        self.plate_reader = Csv_Plate_Reader(self.messages)
        
        self.files = {}
        
    def load(self, datafolder = None):
        
        if datafolder is None:
            datafolder = self.settings.d["datafolder"]
        
        self.read_folder(datafolder)
        self.import_all()
        
    def read_folder(self, datafolder = None):
        
        if datafolder is None:
            datafolder = self.settings.d["datafolder"]
        
        m = self.messages.add("Luetaan kansio " + datafolder, "Dataluku")
        
        for root, dirs, files in os.walk(datafolder):
            for filename in fnmatch.filter(files, self.settings.d["data_filetype_pattern"]):
                filepath = os.path.join(root, filename)
                self.load_file(filepath)
        
        self.datahallinta.tarkista()
        self.messages.set_message_status(m, True)
        
    def load_file(self, filepath):
        m = self.messages.add("Tutkitaan tiedosto " + filepath, "load_file")
        rows = self.plate_reader.read(filepath)
        if len(rows) > 0:
            self.messages.set_message_status(m, True, "Tiedosto on tyyppiä Plate")
            self.datahallinta.lisaa_plate(filepath, rows)
        else:
            status = self.data_reader.check_file(filepath)
            if status is True:
                self.messages.set_message_status(m, True, "Tiedosto on tyyppiä Data")
                add = True
                for data in self.datahallinta.datat:
                    if data == filepath:
                        add = False
                if add is True:
                    self.datahallinta.lisaa_datatiedosto(filepath)
            else:
                self.messages.set_message_status(m, False, "Tiedoston tyyppiä ei tunnistettu")
        
    def import_all(self):
        for data in self.datahallinta.datat:
            m = self.messages.add("Tuodaan mehiäiset " + data, "Dataluku")
            if self.datahallinta.datat[data]["readstatus"] is True:
                self.import_datafile(data)
            else:
                self.messages.set_message_status(m, False, self.datahallinta.str_status(data))
                
    def import_datafile(self, data):
        
        rows = self.data_reader.read(data)
        for row in rows:
            
            row["Sample"] = self.datahallinta.sample(data, row["Well"])
            self.mehilaispesa.lisaa_rivi(row, data)
        
        

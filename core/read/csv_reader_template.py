#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

class Csv_Reader_Template(object):
    
    def __init__(self, messages):
        
        self.messages = messages
        self.columns = []
        self.delimiter = ';'
        self.definitions = {}
        
    def get_dialect(self):
        dialect = csv.excel
        dialect.delimiter = self.delimiter
        dialect.skipinitialspace = True
        return dialect
        
    def check_file(self):
        pass
        
    def read(self, filepath, mehilaispesa):
        m = self.messages.add("Luetaan tiedosto " + filepath, "load")
        try:
            with open(filepath, 'rb') as csvfile:
                reader = csv.reader(csvfile, self.get_dialect())
                
                for i, row in enumerate(reader):
                    
                    if i == 0:
                        self.create_columns(row)
                    else:
                        self.read_row(mehilaispesa, row, filepath)
            
            self.messages.set_message_status(m, True)
            return m
        except Exception, e:
            self.messages.set_message_status(m, False, str(e))
            return m
            
    def create_columns(self, row):
        self.columns = row
            
    def read_row(self, mehilaispesa, row, filepath):
        rivi = {}
        
        try:
            for i, cell in enumerate(row):
                rivi[self.columns[i]] = cell
            mehilaispesa.lisaa_rivi(rivi, filepath)
            
        except Exception, e:
            self.messages.error("row read error: " + str(e), "read_row", ' (row: '+str(row)+')')

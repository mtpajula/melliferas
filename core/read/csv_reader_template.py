#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

class Csv_Reader_Template(object):
    
    def __init__(self, messages):
        
        self.messages = messages
        self.columns = []
        self.delimiter = ';'
        self.definitions = {}
        self.definitions["read_to"] = 0
        self.definitions["column_count"] = 0
        
    def get_dialect(self):
        dialect = csv.excel
        dialect.delimiter = self.delimiter
        dialect.skipinitialspace = True
        return dialect
        
    def check_file(self, filepath):
        
        rows = self.read(filepath, self.definitions["read_to"])
        file_ok = True
        row_ok = False
        
        try:
            for i, row in enumerate(rows):
                if "column_count" in self.definitions:
                    if len(row) != self.definitions["column_count"]:
                        print "column_count"
                        print len(row)
                        print self.definitions["column_count"]
                        return False
                        
                if "cell" in self.definitions:
                    if self.definitions["cell"][0] == i:
                        if self.definitions["column_titles"] == "cell":
                            self.create_columns(row)
                    
                if "row" in self.definitions:
                    if self.definitions["row"][1] == row[self.definitions["row"][0]]:
                        if self.definitions["column_titles"] == "row":
                            self.create_columns(row)
                
                if "column_titles_num" in self.definitions:
                    if i == self.definitions["column_titles_num"]:
                        self.create_columns(row)
        except:
            row_ok = False
        
        if len(self.columns) == 0:
            file_ok = False
        
        print "columns:"
        print self.columns
        
        return file_ok
        
    def read(self, filepath, read_to = None):
        m = self.messages.add("Luetaan tiedosto " + filepath, "load")
        rows = []
        try:
            with open(filepath, 'rb') as csvfile:
                reader = csv.reader(csvfile, self.get_dialect())
                
                for i, row in enumerate(reader):
                    rows.append(self.read_row(row))
                    
                    if read_to is not None:
                        if read_to == i:
                            self.messages.set_message_status(m, True)
                            return rows
                    
            
            self.messages.set_message_status(m, True)
            return rows
        except Exception, e:
            self.messages.set_message_status(m, False, str(e))
            return rows
            
    def create_columns(self, row):
        self.columns = row
            
    def read_row(self, row):
        
        try:
            if len(self.columns) == 0:
                return row
            
            rivi = {}
            
            for i, cell in enumerate(row):
                rivi[self.columns[i]] = cell
            
            return rivi
            
        except Exception, e:
            self.messages.error("row read error: " + str(e), "read_row", ' (row: '+str(row)+')')
            return None
    

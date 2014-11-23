#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

class Csv_Reader_Template(object):
    
    def __init__(self, messages):
        
        self.messages = messages
        self.columns = []
        self.title_column_row = None
        self.delimiter = ';'
        self.definitions = {}
        self.definitions["read_to"] = 10
        self.definitions["column_count"] = 0
        self.definitions["row_to_list"] = False
        
    def get_dialect(self):
        dialect = csv.excel
        dialect.delimiter = self.delimiter
        dialect.skipinitialspace = True
        return dialect
        
    def clear(self):
        self.columns = []
        self.title_column_row = 0
        
    def check_column_title_row(self, row):
        model = self.definitions["title_column"].split(self.delimiter)
        
        row_ok = True
        try:
            for i, cell in enumerate(model):
                if row[i] != cell:
                    row_ok = False
        except:
            row_ok = False
        
        if row_ok is True:
            self.create_columns(row)
        
        return row_ok
        
    def check_file(self, filepath):
        
        rows = self.read(filepath, True)
        if len(rows) > 0:
            return True
        return False
        
    def read(self, filepath, check = False):
        m = self.messages.add("open " + filepath, "load")
        self.clear()
        rows = []
        try:
            with open(filepath, 'rb') as csvfile:
                reader = csv.reader(csvfile, self.get_dialect())
                for i, row in enumerate(reader):
                    
                    if len(self.columns) == 0:
                        self.check_column_title_row(row)
                        if self.definitions["read_to"] is not None:
                            if self.definitions["read_to"] == i:
                                self.messages.set_message_status(m, True)
                                return rows
                    else:
                        rows.append(self.read_row(row))
                        if check is True:
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
            if self.definitions["row_to_list"] is True:
                return row
            
            rivi = {}
            for i, cell in enumerate(row):
                rivi[self.columns[i]] = cell
            
            return rivi
            
        except Exception, e:
            self.messages.error("row read error: " + str(e), "read_row", ' (row: '+str(row)+')')
            return None
    

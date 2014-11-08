#!/usr/bin/env python
# -*- coding: utf-8 -*
import csv

class TemplateWriter(object):
    
    def __init__(self, settings, messages, mehilaispesa):
        
        self.messages = messages
        self.settings = settings
        self.mehilaispesa = mehilaispesa
        self.delimiter = ';'
        self.title_column = []
        
    def get_dialect(self):
        dialect = csv.excel
        dialect.delimiter = self.delimiter
        dialect.skipinitialspace = True
        return dialect
        
    def num(self, num):
        return str(num).replace(".",",")
        
    def write_file(self, data):
        
        filepath = self.settings.get("outfile")
        
        m = self.messages.add("Kirjoitetaan tiedosto " + filepath, "write_data")
        try:
            with open(filepath, 'wb') as csvfile:
                writer = csv.writer(csvfile, self.get_dialect())
                
                self.write_rows(writer, data)
            
            self.messages.set_message_status(m, True)
        except Exception, e:
            self.messages.set_message_status(m, False, str(e))


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from csv_reader_template import Csv_Reader_Template

class Csv_Data_Reader(Csv_Reader_Template):
    
    def __init__(self, messages):
        super(Csv_Data_Reader, self).__init__(messages)
        self.definitions["column_count"] = 8
        self.definitions["row"] = [3,"Target"]
        self.definitions["column_titles"] = "row"
        self.definitions["read_to"] = 10
        
    def load(self, filepath):
        status = self.check_file(filepath)
        
        print "-"*20
        if status is True:
            print " Data-tiedosto"
        else:
            print " Ei ole data-tiedosto"
        print "-"*20

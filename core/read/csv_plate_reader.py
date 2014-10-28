#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from csv_reader_template import Csv_Reader_Template

class Csv_Plate_Reader(Csv_Reader_Template):
    
    def __init__(self, messages):
        super(Csv_Plate_Reader, self).__init__(messages)
        self.definitions["column_count"] = 25
        self.definitions["column_titles"] = "row"
        self.definitions["row"] = [1,"1"]
        self.definitions["read_to"] = 10
        
    def load(self, filepath):
        status = self.check_file(filepath)
        
        print "-"*20
        if status is True:
            print " Plate-tiedosto"
        else:
            print " Ei ole plate-tiedosto"
        print "-"*20

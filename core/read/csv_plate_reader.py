#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from csv_reader_template import Csv_Reader_Template

class Csv_Plate_Reader(Csv_Reader_Template):
    
    def __init__(self, messages):
        super(Csv_Plate_Reader, self).__init__(messages)
        self.definitions["column_count"] = 24
        self.definitions["column_titles"] = "definition_row"
        
    def load(self, filepath, mehilaispesa):
        pass
        

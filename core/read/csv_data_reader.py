#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from csv_reader_template import Csv_Reader_Template

class Csv_Data_Reader(Csv_Reader_Template):
    
    def __init__(self, messages):
        super(Csv_Data_Reader, self).__init__(messages)
        self.definitions["cell"] = [1,4,"Target"]
        self.definitions["column_titles"] = "definition_row"
        
    def load(self, filepath, mehilaispesa):
        pass
        

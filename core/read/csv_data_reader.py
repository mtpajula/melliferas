#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from csv_reader_template import Csv_Reader_Template

class Csv_Data_Reader(Csv_Reader_Template):
    
    def __init__(self, messages):
        super(Csv_Data_Reader, self).__init__(messages)
        self.definitions["title_column"] = ";Well;Fluor;Target;Content;Sample;Cq;SQ"

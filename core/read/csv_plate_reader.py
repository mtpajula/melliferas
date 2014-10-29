#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from csv_reader_template import Csv_Reader_Template

class Csv_Plate_Reader(Csv_Reader_Template):
    
    def __init__(self, messages):
        super(Csv_Plate_Reader, self).__init__(messages)
        self.definitions["title_column"] = ";1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24"
        self.definitions["row_to_list"] = True

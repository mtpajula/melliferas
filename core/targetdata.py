#!/usr/bin/env python
# -*- coding: utf-8 -*

class TargetData(object):
    
    def __init__(self, name, filepath = None, filenum = None):
        self.filepath = filepath
        self.name = name
        self.filenum = filenum
        
        self.status = ""
        self.cq_list = []
        
        self.ct_mean = 0.0
        self.delta_ct = 0.0
        self.standard_deviation = 0.0
        
    def add_cq(self, num):
        self.cq_list.append(num)
        
    def add_str_cq(self, string):
        self.cq_list.append(float(string.replace(",",".")))
        
    def compare(self, name, filepath = None):
        if self.name == name:
            if self.filepath == filepath:
                return True
        return False
        

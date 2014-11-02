#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Settings(object):
    
    def __init__(self):
        self.project_folder = os.getcwd()
        self.d = self.get_default_settings()
                
    def get_default_settings(self):
        
        d = {
                "plate_filetype_pattern" : "*.csv",
                "data_filetype_pattern" : "*.csv",
                "datafolder" : self.get_default_folder(),
                "outfile" : self.get_default_folder() + "out.csv",
                "link_file" : self.get_default_folder() + "links.json",
                "target_limits" : {
                                "Vg" :    {"min" : 15.0, "max" : 25.0},
                                "A1" :    {"min" : 20.0, "max" : 30.0},
                                "Actin" : {"min" : 13.0, "max" : 21.0},
                                "B1" :    {"min" : 23.0, "max" : 27.0},
                                "C2" :    {"min" : 27.0, "max" : 34.0},
                                "RPS49" : {"min" : 15.0, "max" : 25.0}
                                }
            }
        return d
        
    def target_limits(self):
        return self.d["target_limits"]
        
    def merge_settings(self, d_from):
        for setting in d_from:
            self.d[setting] = d_from[setting]
            
    def limit_settings_to_default(self):
        d_old = self.d
        self.d = self.get_default_settings()
        
        for setting in d_old:
            if setting in self.d:
                self.d[setting] = d_old[setting]
    
    def get(self, title = None):
        if title is None:
            return self.d
        return self.d[title]
        
    def set(self, title, value):
        self.d[title] = value
        
    def set_dictionary(self, d):
        self.merge_settings(d)
        
    def get_default_folder(self):
        return self.project_folder + "/data/"
        
        

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
                                "Vg" :    {"min" : 15.0, "max" : 34.0, "dist" : 2.0},
                                "A1" :    {"min" : 18.0, "max" : 34.0, "dist" : 2.0},
                                "Actin" : {"min" : 14.0, "max" : 29.0, "dist" : 3.0},
                                "B1" :    {"min" : 21.0, "max" : 32.0, "dist" : 2.0},
                                "C2" :    {"min" : 26.0, "max" : 36.0, "dist" : 2.0},
                                "RPS49" : {"min" : 14.0, "max" : 28.0, "dist" : 3.0}
                                },
                "target-ref" : {
                                "Vg" : "RPS49",
                                "A1" : "RPS49",
                                "B1" : "RPS49",
                                "C2" : "Actin"
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
        
    def set_outfile_name(self, filename):
        self.d["outfile"] = self.get_default_folder() + filename + ".csv"
        
        

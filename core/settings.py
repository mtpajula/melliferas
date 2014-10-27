#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Settings(object):
    
    def __init__(self):
        self.project_folder = os.getcwd()
        self.d = self.get_default_settings()
                
    def get_default_settings(self):
        
        d = {
                "filetype_pattern" : "*.csv",
                "datafolder" : self.get_default_folder()
            }
        return d
        
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
        
        

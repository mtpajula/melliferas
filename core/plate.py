#!/usr/bin/env python
# -*- coding: utf-8 -*

class PlateHallinta(object):
    
    def __init__(self):
        self.platet = {}
        
    def lisaa_plate(self, filepath, raakadata):
        self.platet[filepath] = raakadata
        
    def linkita(self):
        pass
        #TODO
        
        
        

#!/usr/bin/env python
# -*- coding: utf-8 -*
from settings import Settings
from messages import Messages
from read.dataluku import Dataluku
from mehilaispesa import Mehilaispesa
from datahallinta import DataHallinta

class Mehilaismanageri(object):
    
    def __init__(self):
        self.settings = Settings()
        self.messages = Messages()
        self.mehilaispesa = Mehilaispesa(self.messages)
        self.datahallinta = DataHallinta(self.settings, self.messages)
        
        self.dataluku = Dataluku(self.settings, self.messages, self.mehilaispesa, self.datahallinta)
        
    def load(self):
        self.datahallinta.load()
        for data in self.datahallinta.datat:
            print self.datahallinta.datat[data]["plate"]
            self.dataluku.load_file(self.datahallinta.datat[data]["plate"])
        self.datahallinta.tarkista()
            
    
    
        
        

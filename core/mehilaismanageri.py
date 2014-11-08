#!/usr/bin/env python
# -*- coding: utf-8 -*
from settings import Settings
from messages import Messages
from read.dataluku import Dataluku
from mehilaispesa import Mehilaispesa
from datahallinta import DataHallinta
from write.kirjoitin import BeeWriter
from write.group_kirjoitin import GroupWriter
from laskin import Laskin

class Mehilaismanageri(object):
    
    def __init__(self):
        self.settings = Settings()
        self.messages = Messages()
        
        self.laskin = Laskin(self.settings, self.messages)
        self.mehilaispesa = Mehilaispesa(self.messages, self.laskin)
        self.datahallinta = DataHallinta(self.settings, self.messages)
        
        self.kirjoitin = BeeWriter(self.settings, self.messages, self.mehilaispesa)
        self.ryhmakirjoitin = GroupWriter(self.settings, self.messages, self.mehilaispesa)
        
        
        self.dataluku = Dataluku(self.settings, self.messages, self.mehilaispesa, self.datahallinta)
        
    def load(self):
        self.datahallinta.load()
        for data in self.datahallinta.datat:
            print self.datahallinta.datat[data]["plate"]
            self.dataluku.load_file(self.datahallinta.datat[data]["plate"])
        self.datahallinta.tarkista()
            
    
    
        
        

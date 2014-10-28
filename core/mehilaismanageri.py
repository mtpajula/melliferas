#!/usr/bin/env python
# -*- coding: utf-8 -*
from settings import Settings
from messages import Messages
from read.dataluku import Dataluku
from mehilaispesa import Mehilaispesa
from plate import PlateHallinta

class Mehilaismanageri(object):
    
    def __init__(self):
        self.settings = Settings()
        self.messages = Messages()
        self.mehilaispesa = Mehilaispesa(self.messages)
        self.platehallinta = PlateHallinta(self.settings, self.messages)
        
        self.dataluku = Dataluku(self.settings, self.messages, self.mehilaispesa, self.platehallinta)
        
        
    
    
        
        

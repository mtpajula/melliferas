#!/usr/bin/env python
# -*- coding: utf-8 -*
from targetdata import TargetData

class Mehilainen(object):
    
    def __init__(self, rivi):
        
        self.sample = rivi["Sample"]
        self.rivit = [rivi]
        self.rna_konsentraatio = None
        self.tiedostot = []
        self.nest = rivi["Sample"][0]
        self.treatment = rivi["Sample"][1]
        
    def tiedostosta(self, polku):
        self.tiedostot.append(polku)
        
    def uniikit_tiedostot(self):
        uniikit = []
        for t in self.tiedostot:
            if t not in uniikit:
                uniikit.append(t)
        return uniikit
        
    def tiedoston_numero(self, tiedosto):
        uniikit = self.uniikit_tiedostot()
                
        for i, t in enumerate(uniikit):
            if t == tiedosto:
                return i
        
    def lisaa_rivi(self, rivi):
        self.rivit.append(rivi)
        
    def tulosta_rivit(self):
        for rivi in self.rivit:
            print rivi
            
    def targets(self):
        targets = []
        for i, rivi in enumerate(self.rivit):
            
            if rivi["Target"] != '' and rivi["Cq"] != 'NaN':
                found = False
                for target in targets:
                    
                    if target.compare(rivi["Target"], self.tiedostot[i]) is True:
                        target.add_str_cq(rivi["Cq"])
                        found = True
                
                if found is False:
                    t = TargetData(rivi["Target"], self.tiedostot[i], self.tiedoston_numero(self.tiedostot[i]))
                    t.add_str_cq(rivi["Cq"])
                    targets.append(t)
            
        return targets
            
    def tulosta(self):
        print ""
        print "    Mehiläinen " + self.sample
        print "="*40
        if self.rna_konsentraatio is None:
            print "RNA konsentraatiota ei ole"
        else:
            print "RNA konsentraatiota: " + str(self.rna_konsentraatio)
            
        print "rivejä mehiläisessä " + str(len(self.rivit))
        print "pesä: " + str(self.nest)
        print "treatment: " + str(self.treatment)
        
        print "-- tiedostoista rivejä ---"
        for i, tiedosto in enumerate(self.uniikit_tiedostot()):
            print str(i) + " " + tiedosto
        print ""
        
        

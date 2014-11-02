#!/usr/bin/env python
# -*- coding: utf-8 -*

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
        
    def lisaa_rivi(self, rivi):
        self.rivit.append(rivi)
        
    def tulosta_rivit(self):
        for rivi in self.rivit:
            print rivi
            
    def targets(self):
        targets = {}
        for rivi in self.rivit:
            # 4c3
            if rivi["Target"] != '' and rivi["Cq"] != 'NaN':
                if rivi["Target"] in targets:
                    targets[rivi["Target"]].append(float(rivi["Cq"].replace(",",".")))
                else:
                    targets[rivi["Target"]] = [float(rivi["Cq"].replace(",","."))]
        
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
        for tiedosto in self.tiedostot:
            print tiedosto
        print ""
        
        

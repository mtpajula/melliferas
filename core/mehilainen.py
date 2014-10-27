#!/usr/bin/env python
# -*- coding: utf-8 -*

class Mehilainen(object):
    
    def __init__(self, rivi):
        
        self.sample = rivi["Sample"]
        self.rivit = [rivi]
        self.rna_konsentraatio = None
        self.tiedostot = []
        
        self.treatment = None
        if "Treatment" in rivi:
            self.treatment = rivi["Treatment"]
        
        
    def tiedostosta(self, polku):
        self.tiedostot.append(polku)
        
    def lisaa_rivi(self, rivi):
        self.rivit.append(rivi)
        
    def tulosta_rivit(self):
        for rivi in self.rivit:
            print rivi
            
    def ctmean_per_target(self):
        targets = {}
        for rivi in self.rivit:
            if "Ct mean (r)" in rivi:
                if rivi["Ct mean (r)"] != "":
                    targets[rivi["Target"]] = rivi["Ct mean (r)"]
        
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
        print "treatment: " + self.treatment
        
        print "-- tiedostoista rivejä ---"
        for tiedosto in self.tiedostot:
            print tiedosto
        print ""
        targets = self.ctmean_per_target()
        print " " + "target" + " "*(20 - len("target")) + "Ct mean (r)"
        print "-"*30
        for target in targets:
            spaces = " "*(20 - len(target))
            print " " + target + spaces + targets[target]
        print ""
        
        

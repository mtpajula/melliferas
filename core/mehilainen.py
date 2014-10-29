#!/usr/bin/env python
# -*- coding: utf-8 -*

class Mehilainen(object):
    
    def __init__(self, rivi):
        
        self.sample = rivi["Sample"]
        self.rivit = [rivi]
        self.rna_konsentraatio = None
        self.tiedostot = []
        
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
            
            if rivi["Target"] != '':
                if rivi["Target"] in targets:
                    targets[rivi["Target"]].append(float(rivi["Cq"].replace(",",".")))
                else:
                    targets[rivi["Target"]] = [float(rivi["Cq"].replace(",","."))]
        
        return targets
    
    def count_mean(self, nums):
        '''
        summa = 0.0
        for num in nums:
            summa += num
        return summa / len(nums)
        '''
        return sum(nums) / float(len(nums))
            
    def tulosta(self):
        print ""
        print "    Mehiläinen " + self.sample
        print "="*40
        if self.rna_konsentraatio is None:
            print "RNA konsentraatiota ei ole"
        else:
            print "RNA konsentraatiota: " + str(self.rna_konsentraatio)
            
        print "rivejä mehiläisessä " + str(len(self.rivit))
        print "treatment: " + str(self.treatment)
        
        print "-- tiedostoista rivejä ---"
        for tiedosto in self.tiedostot:
            print tiedosto
        print ""
        targets = self.targets()
        print " " + "target" + " "*(20 - len("target")) + "Ct mean (r)"
        print "-"*30
        for target in targets:
            spaces = " "*(20 - len(target))
            print " " + target + spaces + str(self.count_mean(targets[target]))
        print ""
        
        

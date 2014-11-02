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
    
    def count_mean(self, nums):
        return sum(nums) / float(len(nums))
        
    def targets_count(self, raja_arvot = None):
        targets = self.targets()
        d = {}
        for target in targets:
            laskettu = self.count_mean(targets[target])
            d[target] = {
                        "Ct mean" : laskettu,
                        "limit" : ""
                        }
            
            if raja_arvot is not None:
                if laskettu < raja_arvot[target]['min']:
                    d[target]["limit"] = "under limit"
                elif laskettu > raja_arvot[target]['max']:
                    d[target]["limit"] = "over limit"
                    
        return d
        
            
    def tulosta(self, raja_arvot = None):
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
        targets = self.targets()
        print " " + "target" + " "*(20 - len("target")) + "Ct mean (r)"
        print "-"*50
        # TODO: Käytä targets_count metodia
        for target in targets:
            spaces = " "*(20 - len(target))
            laskettu = self.count_mean(targets[target])
            print " " + target + spaces + str(laskettu),
            
            if raja_arvot is not None:
                spaces = " "*(20 - len(str(laskettu)))
                print spaces,
                if laskettu < raja_arvot[target]['min']:
                    print " ! Alle raja-arvon",
                elif laskettu > raja_arvot[target]['max']:
                    print " ! Yli raja-arvon",
            
            print ""
        print ""
        
        

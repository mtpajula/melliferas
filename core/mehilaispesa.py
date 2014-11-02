#!/usr/bin/env python
# -*- coding: utf-8 -*
from mehilainen import Mehilainen

class Mehilaispesa(object):
    
    def __init__(self, messages, laskin):
        self.nimi = None
        self.messages = messages
        self.laskin = laskin
        self.mehilaiset = {}
        self.treatments = []
        
    def lisaa_rivi(self, rivi, filepath):
        
        if "Sample" in rivi:
            
            if rivi["Sample"] in self.mehilaiset:
                self.mehilaiset[rivi["Sample"]].lisaa_rivi(rivi)
            else:
                apismellifera = Mehilainen(rivi)
                apismellifera.tiedostosta(filepath)
                
                if apismellifera.treatment != None:
                    if apismellifera.treatment not in self.treatments:
                        self.treatments.append(apismellifera.treatment)
                
                self.mehilaiset[rivi["Sample"]] = apismellifera
        else:
            self.messages.error("Ei mehiläisen nimeä rivissä")
            
    def rajaa_treatment(self, treatment):
        rajatut = []
        for bee in self.mehilaiset:
            if self.mehilaiset[bee].treatment == treatment:
                rajatut.append(self.mehilaiset[bee])
        return rajatut
            
    def tulosta_pesatiedot(self):
        print ""
        print "    Mehiläispesä"
        print "="*40
        if self.nimi is None:
            print "Pesällä ei ole nimeä"
        else:
            print "nimi: " + self.nimi
            
        print "mehiläisiä pesässä " + str(len(self.mehilaiset))
        print ""
        
    def empty(self):
        self.mehilaiset.clear()
        del self.treatments[:]
        
    def tulosta_target_data(self, bee):
        targets = bee.targets()
        print " " + "target" + " "*(20 - len("target")) + "Ct mean (r)" + " "*(20 - len("Ct mean (r)")) + "Status"
        print "-"*50
        for target in targets:
            tulokset = self.laskin.ct_mean(target, targets[target])
            spaces = " "*(20 - len(target))
            print " " + target + spaces + str(tulokset["ct_mean"]),
            spaces = " "*(20 - len(str(tulokset["ct_mean"])))
            print spaces + tulokset["status"]

        

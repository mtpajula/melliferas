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
        self.pesat = []
        
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
                        
                if apismellifera.nest not in self.pesat:
                    self.pesat.append(apismellifera.nest)
                
                self.mehilaiset[rivi["Sample"]] = apismellifera
        else:
            self.messages.error("Ei mehiläisen nimeä rivissä")
            
    def rajaa_treatment(self, treatment, bees = None):
        rajatut = []
        if bees is None:
            bees = self.listana()
        for bee in bees:
            if bee.treatment == treatment:
                rajatut.append(bee)
        return rajatut
        
    def rajaa_pesa(self, pesa, bees = None):
        rajatut = []
        if bees is None:
            bees = self.listana()
        for bee in bees:
            if bee.nest == pesa:
                rajatut.append(bee)
        return rajatut
        
    def listana(self):
        lista = []
        for bee in self.mehilaiset:
            lista.append(self.mehilaiset[bee])
        return lista
    
    def rajaa(self, pesa, treatment):
        bees =  self.listana()
        
        if pesa is not None:
            bees = self.rajaa_pesa(pesa, bees)
            
        if treatment is not None:
            bees = self.rajaa_treatment(treatment, bees)
            
        return bees
        
        
    def tulosta_tiedot(self):
        print ""
        for pesa in self.pesat:
            print "    Mehiläispesä " + pesa
            print "="*40
            print "mehiläisiä pesässä " + str(len(self.rajaa_pesa(pesa)))
            print ""
        print "mehiläisiä yhteensä " + str(len(self.mehilaiset))
        print ""
        
    def empty(self):
        self.mehilaiset.clear()
        del self.treatments[:]
        
    def tulosta_target_data(self, bee):
        targets = self.laskin.ct_means(bee.targets())
        targets = self.laskin.delta_ct(targets)
        print " " + "target" + " "*(20 - len("target")) + "Ct mean (r)" + " "*(20 - len("Ct mean")) + "Delta Ct" + " "*(20 - len("Delta Ct")) + "Status"
        print "-"*70
        
        for target in targets:
            spaces = " "*(20 - len(target))
            print " " + target + spaces + str(targets[target]["ct_mean"]),
            spaces = " "*(20 - len(str(targets[target]["ct_mean"])))
            print spaces + str(targets[target]["delta_ct"]),
            spaces = " "*(20 - len(str(targets[target]["delta_ct"])))
            print spaces + targets[target]["status"]

        

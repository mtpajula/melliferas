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
                self.mehilaiset[rivi["Sample"]].tiedostosta(filepath)
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
        
    def poista_mehilainen(self, sample):
        try:
            self.mehilaiset.pop(sample, None)
            return True
        except:
            return False
        
    def listana(self):
        lista = []
        for bee in self.mehilaiset:
            lista.append(self.mehilaiset[bee])
        lista.sort(key = lambda x: x.sample)
        return lista
    
    def rajaa(self, pesa, treatment):
        bees =  self.listana()
        
        if pesa is not None:
            bees = self.rajaa_pesa(pesa, bees)
            
        if treatment is not None:
            bees = self.rajaa_treatment(treatment, bees)
            
        return bees
        
    def target_keskiarvot(self, pesa = None):
        if pesa is None:
            bees = self.listana()
        else:
            bees = self.rajaa(pesa, None)
        
        ddct = {}
        for treatment in self.treatments:
            t_bees = self.rajaa_treatment(treatment, bees)
            ddct[treatment] = self.laskin.group_ct_mean(t_bees)
            
        return ddct
        
    def tulosta_tiedot(self):
        print ""
        for pesa in self.pesat:
            print "    Mehiläispesä " + pesa
            print "="*40
            print "mehiläisiä pesässä " + str(len(self.rajaa_pesa(pesa)))
            print ""
            self.tulosta_target_keskiarvot(pesa)
            print ""
        print "    Kaikki"
        print "="*40
        print "mehiläisiä yhteensä " + str(len(self.mehilaiset))
        print ""
        self.tulosta_target_keskiarvot()
        print ""
        
    def empty(self):
        self.mehilaiset.clear()
        del self.treatments[:]
        del self.pesat[:]
        
    def tulosta_delta_delta_ct(self, means):
        ddct = self.laskin.delta_delta_ct(means)
        print " " + "target" + " "*(20 - len("target")) + "ryhmät" + " "*(20 - len("ryhmät")) + "Delta delta Ct"
        print "-"*50
        for target in ddct:
            spaces = " "*(20 - len(target))
            t =  " " + target + spaces
            for group in ddct[target]:
                spaces = " "*(20 - len(group))
                print t + group + spaces + str(ddct[target][group])
        
    def tulosta_target_keskiarvot(self, pesa = None):
        means = self.target_keskiarvot(pesa)
        means = self.laskin.delta_ct_treatmens(means)
        print " " + "treatment" + " "*(20 - len("treatment")) + "target" + " "*(20 - len("target")) + "Ryhmän Ct mean" + " "*(20 - len("Ryhmän Ct mean")) + "Delta Ct"
        print "-"*70
        for treatment in means:
            spaces = " "*(20 - len(treatment))
            t =  " " + treatment + spaces
            for target in means[treatment]:
                spaces = " "*(20 - len(target))
                print t + target + spaces + str(means[treatment][target]["ct_mean"]),
                spaces = " "*(20 - len(str(means[treatment][target]["ct_mean"])))
                print spaces + str(means[treatment][target]["delta_ct"])
        print ""
        self.tulosta_delta_delta_ct(means)
        
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

        

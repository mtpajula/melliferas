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
        
        treatments = {}
        for treatment in self.treatments:
            t_bees = self.rajaa_treatment(treatment, bees)
            treatments[treatment] = self.laskin.group_ct_mean(t_bees)
            
        return treatments
        
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
        
    def tulosta_delta_delta_ct(self, treatments):
        ddct = self.laskin.delta_delta_ct(treatments)
        self.tulosta_rivi(["Target","Ryhmat","Delta Delta Ct"])
        print "-"*80
        
        for target in ddct:
            for group in ddct[target]:
                self.tulosta_rivi([target,group,ddct[target][group]])
        
    def tulosta_target_keskiarvot(self, pesa = None):
        treatments = self.target_keskiarvot(pesa)
        treatments = self.laskin.delta_ct_treatmens(treatments)
        
        self.tulosta_rivi(["Treatment","Target","Ryhma Ct mean","Keskihajonta","Delta Ct"])
        print "-"*80
        
        for treatment in treatments:
            for target in treatments[treatment]:
                t = treatments[treatment][target]
                self.tulosta_rivi([treatment,target,t.ct_mean,t.standard_deviation,t.delta_ct])
                
        print ""
        self.tulosta_delta_delta_ct(treatments)
        
    def tulosta_target_data(self, bee):
        targets = self.laskin.ct_means(bee.targets())
        targets = self.laskin.delta_ct(targets)
        
        self.tulosta_rivi(["File","Target","Ct mean","Delta Ct","Status"])
        print "-"*80
        
        for target in targets:
            self.tulosta_rivi([target.filenum,target.name,target.ct_mean,target.delta_ct,target.status])
            
    def tulosta_rivi(self, rivi):
        spaces = " "
        for s in rivi:
            print spaces + str(s),
            spaces = " "*(15 - len(str(s)))
        print ""
        

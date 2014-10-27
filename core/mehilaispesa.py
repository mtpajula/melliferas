#!/usr/bin/env python
# -*- coding: utf-8 -*
from mehilainen import Mehilainen

class Mehilaispesa(object):
    
    def __init__(self, messages):
        self.nimi = None
        self.messages = messages
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

        

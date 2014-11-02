#!/usr/bin/env python
# -*- coding: utf-8 -*-
from template import Cli_Template
from tur import Terminal_Ui_Reciever

class Cli_Main(Cli_Template):
    
    def __init__(self, melliferas, argv):
        super(Cli_Main, self).__init__()
        
        self.argv = argv
        self.melliferas = melliferas
        self.melliferas.messages.ui.set(Terminal_Ui_Reciever(), 'cli')
        self.melliferas.load()
        
        self.title = "Päävalikko"
        
        self.commands["viestit"] = self.print_messages
        self.commands["asetukset"] = self.print_settings
        self.commands["lue"] = self.load_data
        self.commands["sample"] = self.read_bee
        self.commands["pesa"] = self.read_nest
        self.commands["treatment"] = self.read_treatments
        self.commands["data"] = self.datahallinta_status
        self.commands["link"] = self.link_plates
        self.commands["kirjoita"] = self.write_file
        
    def print_settings(self):
        print "\n == Asetukset ==> "
        for s in self.melliferas.settings.get():
            w = " " * (30 - len(s))
            print " > " + s + ":" + w + str(self.melliferas.settings.get(s))
    
    def print_messages(self):
        print "\n == Viestit ==> "
        self.melliferas.messages.ui.get('cli').print_messagelist(self.melliferas.messages.m)
        
    def datahallinta_status(self):
        print "\n == datalinkit ==> \n"
        self.melliferas.datahallinta.tulosta_linkit()
        print "\n == platet ==> "
        self.melliferas.datahallinta.tulosta_platet()
    
    def load_data(self):
        self.melliferas.dataluku.load()
        
    def read_nest(self):
        self.melliferas.mehilaispesa.tulosta_pesatiedot()
        
    def write_file(self):
        self.melliferas.kirjoitin.write()
        
    def read_bee(self):
        print ""
        bee = raw_input("Anna mehiläisen nimi: ")
        if bee in self.melliferas.mehilaispesa.mehilaiset:
            self.melliferas.mehilaispesa.mehilaiset[bee].tulosta(self.melliferas.settings.target_limits())
            question = raw_input("Luetaanko raakadatarivit? (k/e): ")
            if question == "k":
                self.melliferas.mehilaispesa.mehilaiset[bee].tulosta_rivit()
        else:
            print "Tuon nimistä mehiläistä ei löytynyt"
        print ""
        
    def read_treatments(self):
        opt = self.select_options(self.melliferas.mehilaispesa.treatments)
        print ""
        bees = self.melliferas.mehilaispesa.rajaa_treatment(self.melliferas.mehilaispesa.treatments[opt])
        print "mehiläisiä treatment -rajauksella: " + str(len(bees))
        print ""
        for bee in bees:
            print " " + bee.sample,
        print ""
        print ""
        
    def link_plates(self):
        
        platet = self.melliferas.datahallinta.platelista()
        
        for data in self.melliferas.datahallinta.datat:
            print "datatiedosto:"
            print data
            print "-"*20
            opt = self.select_options(platet)
            if opt is None:
                print " ! Ei plateja, mistä valita"
                return
            print ""
            self.melliferas.datahallinta.linkita(data, platet[opt])
            print "Linkitetty"
            print ""
        
    def select_options(self, options):
        
        print ""
        for i, name in enumerate(options):
            num = str(i)
            if len(num) == 1:
                num += " "
            
            print " [ " + num,
            print "]: " + name
        print ""
        
        if len(options) > 0:
            syote = raw_input("Valitse listasta: ")
            if syote != "":
                if self.is_int(syote):
                    num = int(syote)
                    if num < len(options) and num >= 0:
                        return num
                    else:
                        print " ! Antamaasi lukua ei ole listassa"
                else:
                    print " ! Et antanut numeroa"
            else:
                print " ! Et antanut mitään"
        return None
        
    def is_int(self, num):
        try:
            int(num)
            return True
        except ValueError:
            return False
        
        
        

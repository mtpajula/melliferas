#!/usr/bin/env python
# -*- coding: utf-8 -*
import os.path, time
import simplejson as json

class DataHallinta(object):
    
    def __init__(self, settings, messages):
        
        self.messages = messages
        self.settings = settings
        self.platet = {}
        self.datat = {}
        
        self.statukset = {
                            "noplategiven" : "Linkitystä ei tehty",
                            "noplate" : "Platetiedostoa ei löytynyt",
                            "noplatedata" : "Platetiedostoa ei ole luettu",
                            "nodata" : "Datatiedostoa ei löytynyt",
                            "noall" : "Tiedostoja ei löytynyt",
                            "allok" : "Ok"
                        }
        
    def lisaa_plate(self, plate_filepath, raakadata):
        
        for r, rivi in enumerate(raakadata):
            for s, solu in enumerate(rivi):
                if solu == '':
                    try:
                        raakadata[r][s] = raakadata[r-1][s]
                    except:
                        pass
        
        self.platet[plate_filepath] = raakadata
        
    def sample(self, data, well):
        for row in self.platet[self.datat[data]["plate"]]:
            if row[0] == well[0]:
                #print well[1:]
                return row[int(well[1:])]
                
        
    def tyhjenna(self):
        self.platet = {}
        self.datat = {}
        
    def lisaa_datatiedosto(self, data_filepath, plate_filepath = None):
        self.datat[data_filepath] = {
                                        "plate" : plate_filepath,
                                        "status" : "noplategiven",
                                        "readstatus" : False
                                    }
        self.tarkista_linkki(data_filepath)
        self.save()
        
    def linkita(self, data_filepath, plate_filepath):
        self.lisaa_datatiedosto(data_filepath, plate_filepath)
        
    def tarkista(self):
        for linkki in self.datat:
            self.tarkista_linkki(linkki)
            
    def platelista(self):
        lista = []
        for plate in self.platet:
            lista.append(plate)
        return lista
            
    def tarkista_linkki(self, linkki):
        
        dataon = True
        if self.status(linkki) is False:
            self.datat[linkki]["status"] = "nodata"
            self.datat[linkki]["readstatus"] = False
            dataon = False

        if self.status(self.datat[linkki]["plate"]) is False:
            if dataon is False:
                self.datat[linkki]["status"] = "noall"
                self.datat[linkki]["readstatus"] = False
            else:
                self.datat[linkki]["status"] = "noplate"
                self.datat[linkki]["readstatus"] = False
            dataon = False
        else:
            if self.datat[linkki]["plate"] in self.platet:
                if self.platet[self.datat[linkki]["plate"]] is None:
                    self.datat[linkki]["status"] = "noplatedata"
                    self.datat[linkki]["readstatus"] = False
                    dataon = False
            else:
                self.datat[linkki]["status"] = "noplatedata"
                self.datat[linkki]["readstatus"] = False
                dataon = False
        
        if dataon is False:
            return
        
        self.datat[linkki]["status"] = "allok"
        self.datat[linkki]["readstatus"] = True
        
    def status(self, filepath):
        if filepath is None:
            return False
        if os.path.isfile(filepath) is True:
            return True
        return False
        
    def str_status(self, data):
        return self.statukset[self.datat[data]["status"]]
    
    def tulosta_linkit(self):
        for data in self.datat:
            print data
            print "    plate:    " + str(self.datat[data]["plate"])
            print "    status:   " + self.statukset[self.datat[data]["status"]]
            
    def tulosta_platet(self):
        for plate in self.platet:
            print ""
            print plate
            print "-"*20
            if self.platet[plate] is None:
                print " ! Tiedosto on lukematta"
            else:
                for rivi in self.platet[plate]:
                    print rivi
        
    def save(self):
        m = self.messages.add("Saving link file", "PlateHallinta")
        try:
            with open(self.settings.get("link_file"), 'w') as outfile:
                json.dump(self.datat, outfile)
            
            self.messages.set_message_status(m, True, "link file saved")
        except Exception, e:
            self.messages.set_message_status(m, False, "link file save failed:" + str(e))

    def load(self):
        m = self.messages.add("Loading  link file", "PlateHallinta")
        
        try:
            with open(self.settings.get("link_file")) as outfile:
                self.datat = json.load(outfile)
                self.tarkista()
            self.messages.set_message_status(m, True, "link file found")
        except Exception, e:
            self.messages.set_message_status(m, False, "No link file: " + str(e))



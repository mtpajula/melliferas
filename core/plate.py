#!/usr/bin/env python
# -*- coding: utf-8 -*
import os.path, time
import simplejson as json

class PlateHallinta(object):
    
    def __init__(self, settings, messages):
        
        self.messages = messages
        self.settings = settings
        self.platet = {}
        self.linkit = {}
        
        self.statukset = {
                            "noplategiven" : "Linkitystä ei tehty",
                            "noplate" : "Platetiedostoa ei löytynyt",
                            "nodata" : "Datatiedostoa ei löytynyt",
                            "noall" : "Tiedostoja ei löytynyt",
                            "allok" : "Ok"
                        }
        
    def lisaa_plate(self, plate_filepath, raakadata):
        self.platet[plate_filepath] = raakadata
        
    def lisaa_datatiedosto(self, data_filepath, plate_filepath = None):
        self.linkit[data_filepath] = {
                                        "plate" : plate_filepath,
                                        "status" : self.statukset["noplategiven"],
                                        "readstatus" : False
                                    }
        self.tarkista_linkki(data_filepath)
        self.save()
        
    def tarkista(self):
        for linkki in self.linkit:
            self.tarkista_linkki(linkki)
            
    def tarkista_linkki(self, linkki):
        
        dataon = True
        if self.status(linkki) is False:
            self.linkit[linkki]["status"] = self.statukset["nodata"]
            self.linkit[linkki]["readstatus"] = False
            dataon = False

        if self.status(self.linkit[linkki]["plate"]) is False:
            if dataon is False:
                self.linkit[linkki]["status"] = self.statukset["noall"]
            else:
                self.linkit[linkki]["status"] = self.statukset["noplate"]
                self.linkit[linkki]["readstatus"] = False
            dataon = False
        
        self.linkit[linkki]["status"] = self.statukset["allok"]
        self.linkit[linkki]["readstatus"] = True
        

    def status(self, filepath):
        if os.path.isfile(filepath) is True:
            return True
        return False
    
    def tulosta_linkit(self):
        for data in self.linkit:
            print data
            print "    plate:    " + self.linkit[data]["plate"]
            print "    status:   " + self.linkit[data]["status"]
        
    def save(self):
        m = self.messages.add("Saving link file", "PlateHallinta")
        try:
            with open(self.settings.get("link_file"), 'w') as outfile:
                json.dump(self.linkit, outfile)
            
            self.messages.set_message_status(m, True, "link file saved")
        except Exception, e:
            self.messages.set_message_status(m, False, "link file save failed:" + str(e))

    def load(self):
        m = self.messages.add("Loading  link file", "PlateHallinta")
        
        try:
            with open(self.settings.get("link_file")) as outfile:
                self.linkit = json.load(outfile)
            
            self.messages.set_message_status(m, True, "link file found")
        except Exception, e:
            self.messages.set_message_status(m, False, "No link file: " + str(e))



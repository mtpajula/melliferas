#!/usr/bin/env python
# -*- coding: utf-8 -*
import csv

class BeeWriter(object):
    
    def __init__(self, settings, messages, mehilaispesa):
        
        self.messages = messages
        self.settings = settings
        self.mehilaispesa = mehilaispesa
        self.delimiter = ';'
        
    def get_dialect(self):
        dialect = csv.excel
        dialect.delimiter = self.delimiter
        dialect.skipinitialspace = True
        return dialect
        
    def write(self):
        
        filepath = self.settings.get("outfile")
        
        m = self.messages.add("Kirjoitetaan tiedosto " + filepath, "write")
        try:
            with open(filepath, 'wb') as csvfile:
                writer = csv.writer(csvfile, self.get_dialect())
                
                writer.writerow(['Sample', 'Nest', 'Treatment', 'Target', 'Ct mean', 'Delta Ct', 'Status'])
                
                for beesample in self.mehilaispesa.mehilaiset:
                    bee = self.mehilaispesa.mehilaiset[beesample]
                    targets = bee.targets()
                    
                    targets = self.mehilaispesa.laskin.ct_means(bee.targets())
                    targets = self.mehilaispesa.laskin.delta_ct(targets)
                    
                    for target in targets:
                        row = []
                        row.append(beesample)
                        row.append(bee.nest)
                        row.append(bee.treatment)
                        row.append(target)
                        row.append(str(targets[target]["ct_mean"]).replace(".",","))
                        row.append(str(targets[target]["delta_ct"]).replace(".",","))
                        row.append(targets[target]["status"])
                        
                        writer.writerow(row)
            
            self.messages.set_message_status(m, True)
        except Exception, e:
            self.messages.set_message_status(m, False, str(e))

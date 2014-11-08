#!/usr/bin/env python
# -*- coding: utf-8 -*
import csv
from template_kirjoitin import TemplateWriter 

class BeeWriter(TemplateWriter):
    
    def __init__(self, settings, messages, mehilaispesa):
        super(BeeWriter, self).__init__(settings, messages, mehilaispesa)
        self.title_column = ['Sample', 'Nest', 'Treatment', 'Target', 'Ct mean', 'Standard deviation', 'Delta Ct', 'Status']
        
    def get_dialect(self):
        dialect = csv.excel
        dialect.delimiter = self.delimiter
        dialect.skipinitialspace = True
        return dialect
        
    def write(self, bees = None):
        if bees is None:
            bees = self.mehilaispesa.listana()
        self.write_file(bees)
        
    def write_rows(self, writer, bees):
        
        writer.writerow(self.title_column)
        
        for bee in bees:
            targets = bee.targets()
            
            targets = self.mehilaispesa.laskin.ct_means(bee.targets())
            targets = self.mehilaispesa.laskin.delta_ct(targets)
            
            for target in targets:
                row = []
                row.append(bee.sample)
                row.append(bee.nest)
                row.append(bee.treatment)
                row.append(target)
                row.append(self.num(targets[target]["ct_mean"]))
                row.append(self.num(targets[target]["standard_deviation"]))
                row.append(self.num(targets[target]["delta_ct"]))
                row.append(targets[target]["status"])
                
                writer.writerow(row)

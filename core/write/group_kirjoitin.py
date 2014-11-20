#!/usr/bin/env python
# -*- coding: utf-8 -*
import csv
from template_kirjoitin import TemplateWriter 

class GroupWriter(TemplateWriter):
    
    def __init__(self, settings, messages, mehilaispesa):
        super(GroupWriter, self).__init__(settings, messages, mehilaispesa)
        self.title_column = ['Nest', 'Treatment', 'Target', 'Group Ct mean', 'Standard deviation', 'Delta Ct']
        self.title_column_ddct = ['Nest', 'Target', 'Group', 'Delta Delta Ct','','']
        
    def write(self, nest = None):
        self.write_file(nest)
        
    def write_rows(self, writer, nest):
        
        if nest is None:
            nest_name = 'All'
        else:
            nest_name = nest
        
        writer.writerow(['','','','','',''])
        writer.writerow(['Nest:',nest_name,'','','',''])
        writer.writerow(['Bees:',str(len(self.mehilaispesa.rajaa(nest, None))),'','','',''])
        writer.writerow(['','','','','',''])
        writer.writerow(self.title_column)
        
        treatments = self.mehilaispesa.target_keskiarvot(nest)
        treatments = self.mehilaispesa.laskin.delta_ct_treatmens(treatments)
        
        for treatment in treatments:
            for target in treatments[treatment]:
                row = []
                row.append(nest_name)
                row.append(treatment)
                t = treatments[treatment][target]
                row.append(t.name)
                row.append(self.num(t.ct_mean))
                row.append(self.num(t.standard_deviation))
                row.append(self.num(t.delta_ct))
                
                writer.writerow(row)
        
        ddct = self.mehilaispesa.laskin.delta_delta_ct(treatments)
        
        writer.writerow(['','','','','',''])
        writer.writerow(self.title_column_ddct)
        
        for target in ddct:   
            for group in ddct[target]: 
                row = []
                row.append(nest_name)
                row.append(target)
                row.append(group)
                row.append(self.num(ddct[target][group]))
                row.append('')
                row.append('')
                
                writer.writerow(row)
            
            
        
        
        

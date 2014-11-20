#!/usr/bin/env python
# -*- coding: utf-8 -*
import numpy as np
from targetdata import TargetData

class Laskin(object):
    
    def __init__(self, settings, messages):
        
        self.messages = messages
        self.settings = settings
        
    def ct_means(self, targets):
        for target in targets:
            self.ct_mean(target)
        return targets
        
    def ct_mean(self, target):
        rajat = self.settings.get("target_limits")
        
        in_limits = []
        for i, cq in enumerate(target.cq_list):
            if cq < rajat[target.name]['min']:
                pass
            elif cq > rajat[target.name]['max']:
                pass
            else:
                in_limits.append(cq)
        
        if len(in_limits) < 1:
            target.status = "All values out of limits"
            return
            
        comparison = 0
            
        diff = len(target.cq_list) - len(in_limits)
        if diff > 0:
            target.status = str(diff) + " out of limits "
        
        target.ct_mean = self.count_mean(in_limits)
        target.standard_deviation = self.count_standard_deviation(in_limits)
        
    def count_mean(self, nums):
        return sum(nums) / float(len(nums))
        
    def count_standard_deviation(self, nums):
        if len(nums) < 2:
            return 0.0
        
        return np.std(nums, ddof=1)
        
    def to_list(self, dictionary):
        l = []
        for d in dictionary:
            l.append(dictionary[d])
        return l
        
    def delta_ct_treatmens(self, treatments):
        for treatment in treatments:
            self.delta_ct(self.to_list(treatments[treatment]))
        return treatments
        
    def delta_ct(self, targets):
        
        target_ref = self.settings.get("target-ref")
        
        for t in targets:
            
            if t.name not in target_ref:
                continue
                
            if t.ct_mean == 0.0:
                continue
            
            tref = None
            for t2 in targets:
                if t2.compare(target_ref[t.name], t.filepath) is True:
                    tref = t2
                    break
            
            if tref is None:
                continue
            
            if tref.ct_mean == 0.0:
                continue
                
            t.delta_ct = t.ct_mean - tref.ct_mean
        
        return targets
        
    def group_ct_mean(self, bees):
        target_means = {}
        
        for bee in bees:
            targets = self.ct_means(bee.targets())
            
            for target in targets:
                if target.ct_mean != 0:
                    if target.name in target_means:
                        target_means[target.name].add_cq(target.ct_mean)
                    else:
                        t = TargetData(target.name)
                        t.add_cq(target.ct_mean)
                        target_means[target.name] = t
        
        for target in target_means:
            t = target_means[target]
            t.ct_mean = self.count_mean(t.cq_list)
            t.standard_deviation = self.count_standard_deviation(t.cq_list)
            
        return target_means
        
    def delta_delta_ct(self, treatments):
        
        target_ref = self.settings.get("target-ref")
        results = {}
        
        for target in target_ref:
            try:
                results[target] = {
                                    "test1" :   treatments["t"][target].delta_ct - treatments["c"][target].delta_ct,
                                    "test2" :   treatments["t"][target].delta_ct - treatments["i"][target].delta_ct,
                                    "control" : treatments["c"][target].delta_ct - treatments["i"][target].delta_ct,
                                }
            except Exception, e:
                self.messages.error("delta-delta-ct, " + target + ": " + str(e))
        
        return results
            
        
        

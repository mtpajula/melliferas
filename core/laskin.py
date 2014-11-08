#!/usr/bin/env python
# -*- coding: utf-8 -*
import numpy as np

class Laskin(object):
    
    def __init__(self, settings, messages):
        
        self.messages = messages
        self.settings = settings
        
    def ct_means(self, targets):
        outdata = {}
        for target in targets:
            outdata[target] = self.ct_mean(target, targets[target])
        return outdata
        
    def ct_mean(self, target, cq_list):
        rajat = self.settings.get("target_limits")
        outdata = {
                    "ct_mean" : 0.0,
                    "status" : "",
                    "delta_ct" : "",
                    "standard_deviation" : ""
                    }
        
        comparison = None
        
        in_limits = []
        for i, cq in enumerate(cq_list):
            if cq < rajat[target]['min']:
                pass
            elif cq > rajat[target]['max']:
                pass
            else:
                in_limits.append(cq)
        
        if len(in_limits) < 1:
            outdata["status"] = "All values out of limits"
            return outdata
            
        comparison = 0
            
        diff = len(cq_list) - len(in_limits)
        if diff > 0:
            outdata["status"] = str(diff) + " out of limits "
        
        del_list = []
        for i, cq in enumerate(in_limits):
            if i != comparison:
                if abs(cq - in_limits[comparison]) > rajat[target]['dist']:
                    del_list.append(cq)
        
        if len(del_list) > 0:
            outdata["status"] = str(len(del_list)) + " too large distance "
        '''
        for d in del_list:
            in_limits.remove(d)
        '''
        outdata["ct_mean"] = self.count_mean(in_limits)
        outdata["standard_deviation"] = self.count_standard_deviation(in_limits)
                    
        return outdata
        
    def count_mean(self, nums):
        return sum(nums) / float(len(nums))
        
    def count_standard_deviation(self, nums):
        if len(nums) < 2:
            return 0
        
        return np.std(nums, ddof=1)
        
    def delta_ct_treatmens(self, ddct):
        ddct_2 = {}
        for treatment in ddct:
            ddct_2[treatment] = self.delta_ct(ddct[treatment])
            
        return ddct_2
        
    def delta_ct(self, meandata):
        
        target_ref = self.settings.get("target-ref")
        
        for target in meandata:
            
            if target not in target_ref:
                continue
                
            if target_ref[target] not in meandata:
                continue
                
            if meandata[target_ref[target]]["ct_mean"] == 0:
                continue
                
            if meandata[target]["ct_mean"] == 0:
                continue
            
            meandata[target]["delta_ct"] = meandata[target]["ct_mean"] - meandata[target_ref[target]]["ct_mean"]
        
        return meandata
        
    def group_ct_mean(self, bees):
        target_means = {}
        
        for bee in bees:
            targets = self.ct_means(bee.targets())
            
            for target in targets:
                
                if target in target_means:
                    target_means[target].append(targets[target]["ct_mean"])
                else:
                    target_means[target] = [targets[target]["ct_mean"]]
        
        ddct_targets = {}
        for target in target_means:
            ddct_targets[target] = {
                                    "ct_mean" : self.count_mean(target_means[target]),
                                    "status" : "",
                                    "delta_ct" : "",
                                    "standard_deviation" : self.count_standard_deviation(target_means[target])
                                }
            #ddct_targets[target] = self.count_mean(target_means[target])
        return ddct_targets
        
    def delta_delta_ct(self, ddct):
        
        target_ref = self.settings.get("target-ref")
        results = {}
        
        for target in target_ref:
            try:
                results[target] = {
                                    "test1" :   ddct["t"][target]["delta_ct"] - ddct["c"][target]["delta_ct"],
                                    "test2" :   ddct["t"][target]["delta_ct"] - ddct["i"][target]["delta_ct"],
                                    "control" : ddct["c"][target]["delta_ct"] - ddct["i"][target]["delta_ct"],
                                }
            except Exception, e:
                self.messages.error("delta-delta-ct, " + target + ": " + str(e))
        
        return results
            
        
        

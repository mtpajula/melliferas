#!/usr/bin/env python
# -*- coding: utf-8 -*

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
                    "delta_ct" : ""
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
                    
        return outdata
        
    def count_mean(self, nums):
        return sum(nums) / float(len(nums))
        
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
            
        
        

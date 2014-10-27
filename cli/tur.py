#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Terminal_Ui_Reciever(object):
        
    def message_added(self, m):
        print "   ... " + m.str() + " ..."
    
    def message_added_to_parent(self, parent):
        if parent.action != "exec" and parent.action != "clean":
            #print parent.action
            w = " " * 20
            
            m = parent.messages[-1]
            
            self.print_message(m, w, False)
        
    def message_status_added(self, m):
        self.print_message(m, "", True, False, False)
        
    def print_message(self, m, sw = "", status = True, as_string = False, mlist = True):
        w = " " * (30 - len(m.str()))
        
        success = ""
        if m.success:
            success += " - "
        else:
            success += " ! "
        
        end = ""
        if status:
            end += " -> "
            if m.reason is None:
                if m.success:
                    end += "ok"
                else:
                    end += "fail"
            else:
                end += m.reason.str()
        
        out = sw + success + m.str() + w + end
        if as_string:
            return out
        print out
        
        if mlist:
            w = " " * 20
            w += sw
            self.print_messagelist(m.messages, w)
            
    def print_messagelist(self, messages, sw = ""):
        for m in messages:
            self.print_message(m, sw)

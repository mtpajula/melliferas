#!/usr/bin/env python
# -*- coding: utf-8 -*


class Message(object):
    
    def __init__(self, default = "", action = None):
        
        self.default = default
        self.action = action
        self.translations = {}
        
        self.messages = []
        
        self.success = True
        self.reason = None
        
    def add_message(self, message):
        self.messages.append(message)
        
    def add_lang(self, lang, translation):
        self.translations[lang] = translation

    def set_status(self, success, reason = None):
        self.success = success
        self.reason = reason
    
    def str(self, lang = None):
        
        if lang in self.translations:
            return self.translations[lang]
            
        if "en" in self.translations:
            return self.translations["en"]
            
        return self.default
        
        
class Ui_Reciever(object):
    
    def __init__(self):
        self.recievers = {}
        self.newest = None
    
    def set(self, ui, title = None):
        
        if ui is None:
            self.unset(self.newest)
            return self.newest
        
        if title is None:
            title = str(len(self.recievers))
        
        self.recievers[title] = ui
        self.newest = title
        return self.newest
        
    def is_set(self, title):
        if title in self.recievers:
            return True
        return False
        
    def is_empty(self):
        if len(self.recievers) > 0:
            return False
        return True
        
    def get(self, title):
        return self.recievers[title]
        
    def unset(self, title):
        del self.recievers[title]
        
    def unset_all(self):
        self.recievers.clear()
        
    def message_added(self, message):
        for ui in self.recievers:
            self.recievers[ui].message_added(message)
    
    def message_added_to_parent(self, parent):
        for ui in self.recievers:
            self.recievers[ui].message_added_to_parent(parent)
    
    def message_status_added(self, message):
        for ui in self.recievers:
            self.recievers[ui].message_status_added(message)


class Messages(object):
    
    def __init__(self):
        self.m = []
        self.translations = {}
        self.lang = "en"
        self.debug = False
        self.ui = Ui_Reciever()
        
    def add(self, default = "", action = None):
        
        message = self.new(default, action)
        self.add_message_object(message)
            
        return message
        
    def error(self, default = "", action = None, reason = None):
        
        message = self.new(default, action)
        message.success = False
        if reason is not None:
            message.reason = self.new(reason, None)
        self.add_message_object(message)
            
        return message
        
    def add_message_object(self, message):
        self.m.append(message)
        
        self.ui.message_added(message)
        
    def add_to(self, parent, default = "", action = None):
        
        message = self.new(default, action)
        parent.add_message(message)
        
        self.ui.message_added_to_parent(parent)
            
        return message
        
    def set_message_status(self, message, success, reason = None):
        
        if reason is None:
            message.set_status(success)
        else:
            message.set_status(success, self.new(reason, None))
        
        self.ui.message_status_added(message)
        
    def new(self, default, action):
        message = Message(default, action)
        
        for lang in self.translations:
            if default in self.translations[lang]:
                message.add_lang(lang, self.translations[lang][default])
                
        return message
        
    def get_current(self):
        return self.get_from(self.m)
        
    def get_current_from(self, message):
        return self.get_from(message.messages)
        
    def get_from(self, m):
        if len(m) > 0:
            return m[-1]
        return None

    def add_translation(self, lang, messages):
        self.translations[lang] = messages
        
    def translate(self, m):
        return m.str(self.lang)
        

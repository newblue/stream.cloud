#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from google.appengine.api import memcache

def google_remove_cache (key):
    ret = memcache.delete (key)
    logging.debug ('google_remove_cache: %s %d', key, ret)
    return ret

def google_set_cache (key, value, lifetime = 360):
    return memcache.set (key, value, lifetime)

def google_get_cache (key):
    return memcache.get (key)

def remove (key):
    return google_remove_cache (key)

def set (key, value, lifetime = 360):
    return google_set_cache (key, value, lifetime)

def get (key):
    return google_get_cache (key)



#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging

PUBLIC_KEY = 'helpme'
PRIVATE_KEY = 'iloveyou'


#PUBLIC_KEY =  70ffc281dbec8dacf4e02e879c6e20a93b1acd59
SECRET =  '72b33fa0385309618132755f814bbd16fb7134af'

import hashlib

def check (public_key):
    _S = hashlib.sha1('_'.join ([public_key, hashlib.sha1(PRIVATE_KEY).hexdigest ()])).hexdigest ()
    c = SECRET == _S
    return c 

def make_passport (domain):
    return hashlib.sha1 ('_'.join ([domain, SECRET])).hexdigest ()

def check_passport (domain, passport):
    c = hashlib.sha1 ('_'.join ([domain, SECRET])).hexdigest () == passport
    return c

if __name__ == '__main__':
    _PUBLIC_KEY = hashlib.sha1(PUBLIC_KEY).hexdigest ()
    _PRIVATE_KEY = hashlib.sha1(PRIVATE_KEY).hexdigest ()
    SECRET = hashlib.sha1 ('_'.join ([_PUBLIC_KEY, _PRIVATE_KEY])).hexdigest ()
    print 'PUBLIC_KEY = ', _PUBLIC_KEY
    print 'SECRET = ', SECRET

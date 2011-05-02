#! /usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import tornado.web
import tornado.wsgi
import wsgiref.handlers
import version
import key
from model import *
import logging
import time, os, urllib
from google.appengine.api import urlfetch

def administrator (method):
    @functools.wraps (method)
    def wrapper (self, *argv, **kwargv):
        go = os.environ.get ('PATH_INFO', None)
        logging.info ('administrator PATH_INFO: [%s]', go)
        if self.check_auth ():
            return method (self, *argv, **kwargv) 
        else:
            self.do_auth (go)
    return wrapper

class BaseHandler (tornado.web.RequestHandler):
    def get_user_locale(self):
        locale = Datum.get ('locale')
        if locale :
            return locale
        if self.current_user and "locale" in self.current_user.prefs:
            # Use the Accept-Language header
            return self.current_user.prefs["locale"]
        return None

class FrontstageHandler (BaseHandler):
    def initialize (self, *argv, **kwargv):
        self.values = {}
        self.values = Datum.get_many ('site_domain', 'site_name', 'site_author', 
                                        'site_slogan', 'site_analytics', 'site_updated')

        if 'site_updated' in self.values and not self.values['site_updated'] :
            self.values['site_updated'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        feed_url = Datum.get ('feed_url')
        if feed_url is None:
             feed_url = '/index.xml'
        elif len(feed_url) == 0:
             feed_url = '/index.xml'
        self.values['feed_url'] = feed_url

class BackstageHandler (BaseHandler):
    def initialize (self, *argv, **kwargv):
        self.values = {}
        self.values = Datum.get_many ( 'site_domain',  'site_author', 
                                        'site_slogan', 'site_updated', default = '')
        self.values['site_name'] = Datum.get ('site_name', 'Stream Cloud')
        logging.info (self.values) 
        if 'site_updated' in self.values and not self.values['site_updated'] :
            self.values['site_updated'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        feed_url = Datum.get ('feed_url')
        if feed_url is None:
             feed_url = '/index.xml'
        elif len(feed_url) == 0:
             feed_url = '/index.xml'
        self.values['feed_url'] = feed_url

        if 'site_domain' in self.values and self.values['site_domain'] is None :
            self.values['site_domain']  = os.environ.get ('HTTP_HOST', None)
       
        self.values ['system_version'] = version.VERSION

    def check_auth (self):
        passport = self.get_cookie ('passport')
        if passport and key.check_passport (self.values.get ('site_domain'), passport):
            return True
        return False

    def do_auth (self, go = None):
        url = '/writer/login'
        if go :
            url = '?go='.join ([url, go])
        self.redirect (url)

    def sync2twitter (self, article):
        site_domain = Datum.get ('site_domain')
        twitter_sync = Datum.get ('twitter_sync')
        if twitter_sync and twitter_sync.lower () ==  'true' and article.is_page == False :
            username = Datum.get ('twitter_account')
            password = Datum.get ('twitter_password')
            if password and username and len(username) and len(password) :
                try:
                    api = twitter.Api (username = username, password = password)
                    status = api.PostUpdate (''.join ([article.title, ' http://', site_domain, '/', article.title_url]))
                except:
                    logging.error ('Sync2Twitter FAIL.')
                    pass
            else:
                logging.debug ('twitter account/password not setup.')


    def ping_google (self):
        site_domain = Datum.get('site_domain')
        site_name = Datum.get('site_name')
        if not site_name or not site_domain :
            logging.debug ('site domain and name not setup.')
            return False 
        site_name_q = urllib.quote (site_name.encode ('utf-8', 'ignore') if isinstance (site_name, unicode) else site_name )
        site_domain_q = urllib.quote (site_domain)
        google_ping = ''.join (['http://blogsearch.google.com/ping?name=', 
                                site_name_q,
                                '&url=http://',
                                site_domain_q,
                                '/&changesURL=http://',
                                site_domain_q,
                                '/index.xml'])
        try:
            result = urlfetch.fetch(google_ping)
            if result.status_code == 200:
                return 'OK: Google Blog Search Ping: %s'%google_ping
            else:
                return 'Reached but failed: Google Blog Search Ping: %s'%google_ping
        except:
            return 'Failed: Google Blog Search Ping: %s'%google_ping


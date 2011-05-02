#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base import *
from model import *
import twitter
import key
import cache
import logging
import urllib
import feedparser
import markdown2 as markdown

class LoginHandler (BackstageHandler):
    def get (self):
        self.render ('backstage/login.html', **self.values)

    def post (self):
        public_key = self.get_argument ('public_key')
        go = self.get_argument ('go', default = '/writer/overview')
        if key.check (public_key):
            self.set_cookie ('passport', key.make_passport (self.values.get ('site_domain', ''))) 
            logging.info ('login ok, go to %s', go)
            self.redirect (go)
        else:
            self.values ['message'] = "Your entered secret passphrase isn't correct"
            self.render ('backstage/login.html', **self.values)

class LogoutHandler (BackstageHandler):
    def get (self):
        self.clear_cookie ('passport')
        self.redirect ('/')
        #self.render ('backstage/logout.html', **self.values)


class OverviewHandler (BackstageHandler):
    @administrator
    def get (self):
        articles = Node.get_all_articles ()
        self.values['articles'] = articles
        self.values['urls'] = Node.get_urls ()
        site_domain = self.values.get ('site_domain', None)
        site_domain_sync = Datum.get ('site_domain_sync', None)
        mentions_web = cache.get ('mentions_web')
        if False and  mentions_web == None and site_domain:
            link = ''.join (['http://blogsearch.google.com/blogsearch_feeds?hl=en&q=',
                             urllib.quote('link:' + site_domain),
                             '&ie=utf-8&num=10&output=atom'])
            mentions_web = feedparser.parse (link)
            cache.set ('mentions_web', mentions_web, 600)
        if mentions_web :
            self.values ['mentions_web'] = mentions_web.entries
        else:
            self.values ['mentions_web'] = None
        mentions_twitter = cache.get('mentions_twitter')
        if False and mentions_twitter is None:    
            q = None
            if site_domain_sync is None:
                q = site_domain
            else:
                q = ' OR '.join ([site_domain, site_domain_sync])
            q = urllib.quote (q)
            try:
                result = urlfetch.fetch('http://search.twitter.com/search.json?q=' + q)
                if result.status_code == 200:
                    mentions_twitter = simplejson.loads(result.content)
                    cache.add('mentions_twitter', mentions_twitter, 600)
            except:
                mentions_twitter = None
        if mentions_twitter and len(mentions_twitter['results']) > 0:
            self.values['mentions_twitter'] = mentions_twitter['results']
        else:
            self.values['mentions_twitter'] = None
        self.render ('backstage/overview.html', **self.values)

class SettingsHandler (BackstageHandler):
    @administrator
    def get (self):
        site_domain_sync = Datum.get ('site_domain_sync')
        site_default_format = Datum.get ('site_default_format', 'markdown')
        twitter_sync = Datum.get ('twitter_sync')
        twitter_account = None
        twitter_password = None
        if twitter_sync and twitter_sync == 'True':
            twitter_sync = True
            twitter_account = Datum.get ('twitter_account')
            twitter_password = Datum.get ('twitter_password')
        else:
            twitter_sync = False
        self.values ['twitter_sync'] = twitter_sync
        self.values ['twitter_account'] = twitter_account
        self.values ['twitter_password'] = twitter_password
        self.values ['site_domain_sync'] = site_domain_sync
        self.values ['site_default_format'] = site_default_format
        self.values ['site_analytics'] = Datum.get ('site_analytics')
        self.render ('backstage/settings.html', **self.values)

    @administrator
    def post (self):
        Datum.set ('site_domain', self.get_argument ('site_domain'))
        Datum.set ('site_domain_sync', self.get_argument ('site_domain_sync', ''))
        Datum.set ('site_name', self.get_argument ('site_name', ''))
        Datum.set ('site_author', self.get_argument ('site_author', ''))
        Datum.set ('site_slogan', self.get_argument ('site_slogan', ''))
        Datum.set ('site_analytics', self.get_argument ('site_analytics', ''))
        Datum.set ('site_default_format', self.get_argument ('site_default_format', ''))
        Datum.set ('twitter_sync', 'True' if self.get_argument ('twitter_sync', 'False') == 'True' else 'False')
        Datum.set ('twitter_account', self.get_argument ('twitter_account', ''))
        Datum.set ('twitter_password', self.get_argument ('twitter_password', ''))
        Datum.set ('feed_url', self.get_argument ('feed_url', '/index.xml'))
        self.redirect ('/writer') 

class WriteHandler (BackstageHandler):
    @administrator
    def get (self, key = None):
        article = Node.get_by_key (key)
        site_default_format = Datum.get ('site_default_format', 'markdown')
        self.values ['site_default_format'] = site_default_format
        self.values ['format'] = site_default_format
        self.values ['article'] = article
        self.render ('backstage/write.html', **self.values)

    @administrator
    def post (self):
        self.redirect ('/writer') 

class RemoveHandler (BackstageHandler):
    @administrator
    def get (self, key = None):
        article = None
        if key :
            article = Node.get_by_key (key)
        if article :
            article.delete ()
        self.redirect ('/writer/overview')
            

class SyncHandler (BackstageHandler):
    @administrator
    def get (self):
        self.redirect ('/writer')

    @administrator
    def post (self, key = None):
        site_domain = Datum.get('site_domain')
        site_domain_sync = Datum.get('site_domain_sync')
        site_name = Datum.get('site_name')
        site_author = Datum.get('site_author')
        site_slogan = Datum.get('site_slogan')
        site_analytics = Datum.get('site_analytics')
        site_default_format = Datum.get('site_default_format', 'markdown')

        page = 0
        site_default_format = Datum.get('site_default_format')
        content = self.get_argument ('content', '')
        sync = False
        if key:
            article = Node.get_by_key (key)
            if article.format not in CONTENT_FORMATS :
                article.format = site_default_format
        else:
            article = Node ()
            sync = True
            new = True

        article.title = self.get_argument('title', None)
        article.title_link = self.get_argument('title_link', None)
        article.title_url = self.get_argument('title_url', None)
        article.parent_url = self.get_argument('parent_url', None)
        article.content = self.get_argument('content', '')
        article.article_set = self.get_argument('article_set', None)
        article.format = self.get_argument('format', 'markdown')
        if article.format not in CONTENT_FORMATS:
          article.format = site_default_format
        article.content_formatted = markdown.markdown (article.content) if article.format == 'markdown' else None

        is_page = self.get_argument ('is_page')
        article.is_page = True if is_page == 'True' else False
        is_for_sidebar = self.get_argument ('is_for_sidebar')
        article.is_for_sidebar = True if is_for_sidebar == 'True' else False
        article.save()
        self.values['site_default_format'] = site_default_format
        self.values['article'] = article
        self.values['format'] = article.format if article else site_default_format
        if not article.is_page :
            self.sync2twitter (article)
            self.ping_google () 
        self.render ('backstage/write.html', **self.values)

class QuickFindHandler (BackstageHandler):
    @administrator
    def post (self):
        pass

class PingHandler (BackstageHandler):
    def get(self):
        self.ping_google ()


#! /usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import memcache
import datetime, logging

from textutils import plaintext2html
__ALL__ = ['CONTENT_FORMATS', 'Node', 'Datum']

CONTENT_FORMATS = set(['html', 'txt', 'markdown'])

class Node (db.Model):
    title = db.StringProperty(required=False, indexed=True)
    title_link = db.StringProperty(required=False, indexed=True)
    title_url = db.StringProperty(required=False, indexed=True)
    parent_url = db.StringProperty(required=False, indexed=True)
    is_page = db.BooleanProperty(required=True, default=False)
    is_for_sidebar = db.BooleanProperty(required=True, default=False)
    content = db.TextProperty()
    content_formatted = db.TextProperty()
    article_set = db.StringProperty(required=False, indexed=True)
    format = db.StringProperty(required=True, default='html', indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    hits = db.IntegerProperty(default=0)
    hits_feed = db.IntegerProperty(default=0)

    def format_content (self):
        format = self.format.strip().lower ()
        if format == 'markdown' :
            return self.content_formatted
        elif format == 'txt':
            return plaintext2html (self.content)
        else:
            return self.content

    def save (self):
        self.last_modified = datetime.datetime.now ()
        self.put ()
        obsolete = ['archive', 'all_articles', 'archive_output', 'feed_output', 'index', 
                    'index_output', 'writer_articles', 'writer_urls']
        memcache.delete_multi(obsolete)

    @staticmethod
    def get_articles (order = '-created', all = False):
        key = 'articles'
        if order :
            key = '_'.join ([key, order])
        articles = memcache.get (key)
        if articles != None:
            return articles
        query = Node.all ()
        query = query.filter ('is_page', False)
        if order :
            query = query.order (order)
        if query.count () :
            memcache.set (key, query, 86400)
        return query

    @staticmethod
    def get_all_articles ():
        key = 'all_articles'
        query = memcache.get (key)
        if query != None:
            return query 
        query = Node.all ()
        if query.count () :
            memcache.set (key, query, 86400)
        return query

    @staticmethod
    def get_article (url = None):
        if url :
            query = Node.all ()
            query = query.filter ('title_url', url.strip())
            return query.get ()
        else:
            return None

    @staticmethod
    def get_pages ():
        query = Node.all ()
        query = query.filter ('is_page', True).filter('title !=', None).filter ('is_for_sidebar', True).order ('-title')
        return query 

    def get_related (self, limit = 10, order = '__key__'):
        if ( isinstance (self.article_set, str) or isinstance (self.article_set, unicode) ) and len(self.article_set) > 0:
            query = Node.all ()
            query = query.filter ('article_set', self.article_set.strip()).filter('__key__ !=', self.key()).order (order)
            return query.fetch (limit)
        else:
            return None

    def get_parent (self):
        if self.parent_url and len (self.parent_url) :
            query = Node.all ()
            query = query.filter ('title_url', self.parent_url)
            return query.get ()
        else:
            return None

    @staticmethod
    def get_article_set (self):
        if isinstance (self.article_set, str) or isinstance (self.article_set, unicode) :
            query = Node.all ()
            query = query.filter ('article_set', self.article_set.strip()).order ('created')
            return query
        else:
            return None

    @staticmethod
    def get_by_key (key):
        article = None
        if key :
            article = db.get(db.Key(key))
        return article

    @staticmethod
    def get_urls ():
        key = 'writer_urls'
        urls = memcache.get (key)
        if isinstance (urls, list):
            return urls
        urls = []
        nodes = Node.all ()
        for node in nodes :
            urls.append (node.title_url)
        if len (urls) :
            memcache.set (key, urls, 86400)
        return urls

class Comment(db.Model):
    author_name = db.StringProperty(required=False, indexed=True)
    author_email = db.StringProperty(required=False, indexed=True)
    author_site = db.StringProperty(required=False, indexed=True)
      
class Datum(db.Model):
    name = db.StringProperty(required=False, indexed=True)
    substance = db.TextProperty()
    @staticmethod
    def get_many (*argv, **kwargv):
        values = {}
        default = kwargv.get ('default', '')
        logging.debug ('Datum.get_many: default = %s', default) 
        for key in argv:
            values[key] = Datum.get (key, default)
        return values

    @staticmethod
    def get(name, default = ''):
        key = '_'.join (['datum', name]) 
        value = memcache.get(key)
        if value == None:
            value = default
            query = Datum.all ()
            query = query.filter ('name', name)
            if query.count() > 0 :
                one = query.get ()
                value = one.substance
                logging.debug ('%s %s', key, value)
                memcache.delete(key)
                memcache.set(key, value, 86400)
        logging.info ('Datum.get: %s %s', name, value)
        return value

    @staticmethod 
    def set(name, value):
        query = Datum.all ()
        query = query.filter ('name', name)
        datum = None
        if query.count() == 1:
            datum = query.get ()
        else:
            datum = Datum()
            datum.name = name
        datum.substance = value
        datum.put()
        key = '_'.join (['datum', name]) 
        memcache.delete(key)
        memcache.set(key, datum.substance, 86400)
 

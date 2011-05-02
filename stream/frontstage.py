#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base import *
from model import *
import logging
import os
import cache
import time

class HomeHandler (FrontstageHandler):
    def head (self):
        pass

    def get (self):
        articles = Node.get_articles ()
        pages =  Node.get_pages ()
        self.values['articles'] = articles
        self.values['pages'] = pages
        self.values['page_type'] = 'home' 
        self.render ('frontstage/index.html', **self.values)
        
class ArchiveHandler (FrontstageHandler):
    def get (self):
        articles = Node.get_articles ()
        pages = Node.get_pages ()
        self.values['page_type'] = 'archive' 
        self.values['articles'] = articles
        self.values['pages'] = pages
        self.render ('frontstage/index.html', **self.values)

class TopHandler (FrontstageHandler):
    def get (self):
        articles = Node.get_articles (order = 'hits')
        pages = Node.get_pages ()
        self.values ['page_type'] = 'top'
        self.values ['articles'] = articles
        self.values ['pages'] = pages
        self.render ('frontstage/index.html', **self.values)

class ArticleHandler (FrontstageHandler):
    def get (self, url):
        article = Node.get_article (url)
        if article is None :
            self.render ('frontstage/404.html')
            return
        pages = Node.get_pages ()
        self.values ['article'] = article
        self.values ['pages'] = pages
        self.values ['related'] = article.get_related ()
        self.values ['parent'] = article.get_parent ()
        self.render ('frontstage/article.html', **self.values)


class AtomFeedHandler (FrontstageHandler):
    def get (self):
        articles = Node.get_articles ()
        self.values ['articles'] = articles
        self.set_header ('Content-Type', 'text/xml; charset=UTF-8')
        self.render ('frontstage/atom.xml', **self.values)

class SetAtomFeedHandler (FrontstageHandler):
    def get (self):
        set = self.get_argument ('set') 
        articles = Node.get_article_set (set)
        self.values['articles'] = articles
        self.render ('frontstage/atom.xml', **values)


class AtomSitemapHandler (FrontstageHandler):
    def get (self):
        articles = Node.get_articles (order = 'last_modified')
        self.values['articles'] = articles
        self.set_header ('Content-Type', 'text/xml; charset=UTF-8')
        self.render('frontstage/sitemap.xml', **self.values)

class RobotsHandler (FrontstageHandler):
    def get (self):
        self.set_header ('Content-Type', 'text/plain; charset=UTF-8')
        self.render ('frontstage/robots.txt')

class HitFeedHandler (FrontstageHandler):
    def get (self, key = None):
        article = Node.get_by_key (key) 
        if article:
            article.hits_feed = article.hits_feed + 1
            article.put()
        self.redirect ('/img/1x1.gif')

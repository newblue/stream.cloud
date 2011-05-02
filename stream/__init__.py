#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.wsgi
import tornado.locale
import wsgiref.handlers
import frontstage, backstage
import os 

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "xsrf_cookies": True,
    'debug' : True,
}

application = tornado.wsgi.WSGIApplication ([
        ('/writer', backstage.OverviewHandler),
        ('/writer/login', backstage.LoginHandler),
        ('/writer/logout', backstage.LogoutHandler),
        ('/writer/overview', backstage.OverviewHandler),
        ('/writer/settings', backstage.SettingsHandler),
        ('/writer/new', backstage.WriteHandler),
        ('/writer/save', backstage.SyncHandler),
        ('/writer/ping', backstage.PingHandler),
        ('/writer/update/([0-9a-zA-Z\-\_]+)', backstage.SyncHandler),
        ('/writer/edit/([0-9a-zA-Z\-\_]+)', backstage.WriteHandler),
        ('/writer/remove/([0-9a-zA-Z\-\_]+)', backstage.RemoveHandler),
        ('/writer/quickfind', backstage.QuickFindHandler),

        ('/archive', frontstage.ArchiveHandler),
        ('/top', frontstage.TopHandler),
        ('/index.xml', frontstage.AtomFeedHandler),
        ('/set.xml', frontstage.SetAtomFeedHandler),
        ('/sitemap.xml', frontstage.AtomSitemapHandler),
        ('/robots.txt', frontstage.RobotsHandler),
        ('/', frontstage.HomeHandler),
        ('/hit/([0-9a-zA-Z\-\_]+)', frontstage.HitFeedHandler),
        ('/([0-9a-zA-Z\-\.]+)', frontstage.ArticleHandler)
], **settings)

def run ():
    tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "translations"))
    tornado.locale.set_default_locale ('zh_CN')
    wsgiref.handlers.CGIHandler().run(application)

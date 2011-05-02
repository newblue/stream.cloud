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
        (r'/writer', backstage.OverviewHandler),
        (r'/writer/login', backstage.LoginHandler),
        (r'/writer/logout', backstage.LogoutHandler),
        (r'/writer/overview', backstage.OverviewHandler),
        (r'/writer/settings', backstage.SettingsHandler),
        (r'/writer/new', backstage.WriteHandler),
        (r'/writer/save', backstage.SyncHandler),
        (r'/writer/ping', backstage.PingHandler),
        (r'/writer/update/([0-9a-zA-Z\-\_]+)', backstage.SyncHandler),
        (r'/writer/edit/([0-9a-zA-Z\-\_]+)', backstage.WriteHandler),
        (r'/writer/remove/([0-9a-zA-Z\-\_]+)', backstage.RemoveHandler),
        (r'/writer/quickfind', backstage.QuickFindHandler),

        (r'/archive', frontstage.ArchiveHandler),
        (r'/top', frontstage.TopHandler),
        (r'/index.xml', frontstage.AtomFeedHandler),
        (r'/set.xml', frontstage.SetAtomFeedHandler),
        (r'/sitemap.xml', frontstage.AtomSitemapHandler),
        (r'/robots.txt', frontstage.RobotsHandler),
        (r'/', frontstage.HomeHandler),
        (r'/hit/([0-9a-zA-Z\-\_]+)', frontstage.HitFeedHandler),
        (r'/([%0-9a-zA-Z\-\.]+)', frontstage.ArticleHandler)
], **settings)

def run ():
    tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "translations"))
    tornado.locale.set_default_locale ('zh_CN')
    wsgiref.handlers.CGIHandler().run(application)

#! /usr/bin/env python
# -*- coding: utf-8 -*-
import web
import template

class helloworld:
    def GET (self):
        return 'hello world'

URLS = (
        '/', 'helloworld'
        )

def main ():
    application = web.application (URLS, globals ())
    return application.cgirun ()


if __name__ == '__main__' :
    main ()



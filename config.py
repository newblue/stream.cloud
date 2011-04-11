#! /usr/bin/env python
# -*- coding: utf-8 -*-

import exts, web, logging

VERSION = 'beta'
DEBUG = False

server = web.ctx.env.get ('SERVER_SOFTWARE', '') 
logging.info('SERVER_SOFTWARE: [%s]', server)
DEBUG = (server.find('Development/1.0') != -1)

if DEBUG :
    logger = logger.getLogger ()
    logger.setLevel (logging.DEBUG)








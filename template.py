#! /usr/bin/env python
# -*- coding: utf-8 -*-

__ALL__ = ['get']
from jinja2 import Environment, FileSystemLoader 

env = Environment (loader = FileSystemLoader ('../templates/'))
get = env.get_template

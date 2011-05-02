#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re, cgi
re_string = re.compile(r'(?P<htmlchars>[<&>])|(?P<space>^[ \t]+)|(?P<lineend>\r\n|\r|\n)|(?P<protocal>(^|\s)((http|ftp)://.*?))(\s|$)', re.S|re.M|re.I)
TAGSTOP = 4
def do_sub(m):
    c = m.groupdict()
    if c['htmlchars']:
        return cgi.escape(c['htmlchars'])
    if c['lineend']:
        return '<br>'
    elif c['space']:
        t = m.group().replace('\t', '&nbsp;'*TABSTOP)
        t = t.replace(' ', '&nbsp;')
        return t
    elif c['space'] == '\t':
        return ' '*TABSTOP;
    else:
        url = m.group('protocal')
        if url.startswith(' '):
            prefix = ' '
            url = url[1:]
        else:
            prefix = ''
        last = m.groups()[-1]
        if last in ['\n', '\r', '\r\n']:
            last = '<br/>'
        return '%s<a href="%s">%s</a>%s' % (prefix, url, url, last)

def plaintext2html(text):
    return re.sub(re_string, do_sub, text)

__ALL__ = ['plaintext2html']

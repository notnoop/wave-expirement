#!/usr/bin/env python
# encoding: utf-8
"""
worldcat.py

Created by Mahmood Ali on 2009-11-20.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os

import logging, re, urllib

from waveapi import events
from waveapi import robot
from waveapi import document

APP_NAME = "notnoop-wave"
GADGET_URL = "http://%s.appspot.com/public/gadget.xml" % APP_NAME

KEYS = ('oclc', 'isbn')
WORLDCAT = re.compile('((' + "|".join(KEYS) + '):(\S*))')

WORLDCAT_URL = 'http://www.worldcat.org'

def OnBlipSubmitted(properties, context):
    blip = context.GetBlipById(properties['blipId'])
    doc = blip.GetDocument()
    contents = doc.GetText()
    for m in WORLDCAT.finditer(contents):
        key = m.group(2)
        value = m.group(3)
        link = '%s/%s/%s' % (WORLDCAT_URL, key, value)
        r = document.Range(m.start(), m.end())
        doc.SetTextInRange(r, value)
        end = m.start() + len(value)
        doc.SetAnnotation(document.Range(m.start(), end),
            "link/manual", link)
        gadget = document.Gadget(url=GADGET_URL, props= {'query' : ('%s:%s') % (key , value)})
        doc.InsertElement(end, gadget)

def getRobot():
    mybot = robot.Robot('NotNoop-Worldcat',
        version = 1,
        image_url="http://notnoop-wave.appspot.com/public/Icon.png",
        profile_url="http://www.notnoop.com")

    mybot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    return mybot

def main():
    mybot = getRobot()
    mybot.Run(debug=True)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

# MIT
# Copyright (c) <year> <copyright holders>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

# built on:
# https://github.com/seb-m/pyinotify

# Based on:
# https://github.com/seb-m/pyinotify/blob/master/python2/examples/chain.py
import pyinotify
import os.path
import re
import logging

class Log(pyinotify.ProcessEvent):
    def my_init(self, fileobj):
        """
        Method automatically called from ProcessEvent.__init__(). Additional
        keyworded arguments passed to ProcessEvent.__init__() are then
        delegated to my_init(). This is the case for fileobj.
        """
        self._fileobj = fileobj

    def process_default(self, event):
        # we want the full path
        filepath = event.pathname
        logging.info("found filepath: %s", filepath)
        # we only care about files, not dirs
        #if not pyinotify.IN_ISDIR:
        if not os.path.isdir(filepath):
            # but we need to split the filename from the filepath
            path, suffix = os.path.split(event.pathname)
            logging.info("found path: %s and suffix: %s", path, suffix)
            # check for our match
            match = re.match('^_',suffix)
            # if we match 
            if match:
                # log it
                self._fileobj.write(str(filepath) + '\n')
                # flush
                self._fileobj.flush()
            else:
                logging.warning("new creation is not a match")
        else:
            logging.warning("new creation is a dir: %s", filepath)

# this is nice for debugging  when not run as a service
class TrackCreate(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        # we want the full path
        filepath = event.pathname
        logging.info("Processed a new creation: %s", filepath)

    def process_default(self, event):
        logging.info("found message: %s", self._msg)


#==================================================================
# the script
#==================================================================
# our variables
ourlog = '/var/log/newfiles.log'
watchdir = '/home'

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

# define the output file
# we append to logging there
fo = file(ourlog, 'a')

try:

    # lets start a watch manager
    wm = pyinotify.WatchManager()

    # It is important to pass named extra arguments like 'fileobj' used for the output file/log.
    handler = TrackCreate(Log(fileobj=fo), msg='Watch triggered')

    # start the notifier
    notifier = pyinotify.Notifier(wm, default_proc_fun=handler)

    # define what is being watched - in this case just creation, just /home, just files, and only those starting with an underscore
    wm.add_watch(watchdir, pyinotify.IN_CREATE, rec=True, auto_add=True)

    # be an active sentry
    notifier.loop()

# log exceptions
except pyinotify.NotifierError, err:
    print >> sys.stderr, err



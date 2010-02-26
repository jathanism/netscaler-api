#!/usr/bin/env python
# -*- coding: utf-8 -*-

# module netscaler.py
#
# Copyright (c) 2010 Jathan McCollum
#
# Special thanks to Allen Sanabria (asanabria@linuxdynasty.org) for the initial
# work on getting the API working with python-suds. 
#
# Original post: http://tinyurl.com/yl4o6vq
#

"""
A container for interacting with a Citrix NetScaler application delivery
controller, utilizing the SOAP API to execute commands. 
"""

__author__ = 'Jathan McCollum <jathan+bitbucket@gmail.com>'
__version__ = '0.1'

import logging
from suds.client import Client, WebFault
from suds.xsd.doctor import Import, ImportDoctor

try:
    import psyco
    psyco.full()
except ImportError:
    pass

# Register suds.client as a console handler... and disable it.
logging.basicConfig(level=logging.ERROR)
logging.getLogger('suds.client').setLevel(logging.ERROR)
logging.disable(logging.ERROR)

DEBUG = False
DEFAULT_WSDL = 'NSConfig.wsdl'


__all__ = ['API', 'InteractionError']


class InteractionError(Exception): 
    """Generic API error"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class API(object):
    """
    Pass any kwargs to init that you would to the suds.client.Client constructor.
    A little bit of magic is performed with the ImportDoctor to cover missing
    types used in the WSDL.

        * If you specify wsdl, this file will be pulled from the default http URL
        * If you specify wsdl_url, it will override the wsdl file. Local
         "file://" URLs work just fine.

    To save time for re-usable code, it is a good idea subclassing this to
    create methods for commonly used commands in your application. Example:

        class MyAPI(API):
            def __init__(self, **kwargs):
                API.__init__(self, **kwargs)

            def change_password(self, username, newpass):
                return self.run("setsystemuser_password", 
                    **dict(username=username, password=newpass))

    """
    def __init__(self, host=None, wsdl_url=None, soap_url=None, wsdl=DEFAULT_WSDL, **kwargs):
        """Creates the suds.client.Client object and loads the WSDL."""
        self.host = host
        self.wsdl = wsdl
        self.wsdl_url = wsdl_url or "http://%s/api/%s" % (self.host, self.wsdl)
        self.soap_url = soap_url or "http://%s/soap/" % self.host

        # fix missing types with ImportDoctor, otherwise we get:
        # suds.TypeNotFound: Type not found: '(Array, # http://schemas.xmlsoap.org/soap/encoding/, )
        self._import = Import('http://schemas.xmlsoap.org/soap/encoding/')
        self._import.filter.add("urn:NSConfig")
        self.doctor = ImportDoctor(self._import)

        for key, value in kwargs.items():
            # set attributes, but don't reset explicit ones.
            if not hasattr(self, key):
                if DEBUG: print "setting %s to %s" % (key, value)
                setattr(self, key, value)

        if DEBUG:
            print 'wsdl_url:', self.wsdl_url
            print 'soap_url:', self.soap_url

        self.client = Client(self.wsdl_url, doctor=self.doctor, location=self.soap_url, **kwargs)
        self.logged_in = False

    def __repr__(self):
        return u'<NetScaler:API host:%s user:%s logged_in:%s>' % (self.host,
                                                                  self.username,
                                                                  self.logged_in)

    def __str__(self):
        """Print me!"""
        return str(self.client)

    def login(self):
        """Performs API login."""
        resp = self.client.service.login(username=self.username, password=self.password)
        if resp.rc != 0:
            raise InteractionError(resp.message)

        if DEBUG: print resp.message
        self.logged_in = True

        return True

    def logout(self):
        """Performs API logout."""
        resp = self.client.service.logout()
        if resp.rc != 0:
            raise InteractionError(resp.message)

        if DEBUG: print resp.message
        self.logged_in = False

        return True

    def run(self, command, **kwargs):
        """Runs the equivalent of client.service.command(**kwargs)"""
        if not self.logged_in:
            if DEBUG: print 'not logged in; logging you in'
            self.login()

        resp = getattr(self.client.service, command)(**kwargs)
        if resp.rc != 0:
            raise InteractionError(resp.message)

        return resp

import unittest
import cherrypy
from cherrypy.test import helper
import sys
import logging
import threading
import warnings

#decorator import for RESTServer setup
from WMQuality.WebTools.RESTServerSetup import DefaultConfig
from WMCore.WebTools.Root import Root

if hasattr( helper.CPWebCase, 'test_gc'):
    del helper.CPWebCase.test_gc
class RESTBaseUnitTest(helper.CPWebCase):
    globalInstances = []
    rt = None
    def setUp(self, initRoot = True):
        # Don't pull in couchapp if we need to
        #   do we really need this? Everyone should have the same
        #   dev environment
        if hasattr(self, 'schemaModules') and self.schemaModules:
            from WMQuality.TestInitCouchApp import TestInitCouchApp as TestInit
        else:
            from WMQuality.TestInit import TestInit
            
        self.testInit = TestInit(__file__)
        self.testInit.setLogging() # logLevel = logging.SQLDEBUG
        self.testInit.setDatabaseConnection( destroyAllDatabase = True )
        myThread = threading.currentThread()
        self.config.setDBUrl(myThread.dbFactory.dburl)
        if hasattr(self, 'schemaModules') and self.schemaModules:
            self.testInit.setSchema(customModules = self.schemaModules,
                                    useDefault = False)
        self.initRoot = initRoot
        if initRoot:
            # the root object we're gonna test
            self.rt = Root(self.config)
            # obnoxious thing to match the cherrypy harness
            # the actual startup happens in setup_class()
            self.__class__.rt = self.rt
            # fires up the test case
            self.setup_class()
                
    def setup_server(cls):
        if cls.rt:
            cls.rt.start(blocking=False, start_engine=False)
    setup_server = classmethod(setup_server)
        
    def tearDown(self):
        if self.initRoot:
            if hasattr(self, 'supervisor'):
                self.teardown_class()
        if hasattr(self, 'schemaModules') and self.schemaModules:
            self.testInit.clearDatabase()
        self.config = None
        return
    
    def initialize(self):
        """
        i.e.
        
        self.config = DefaultConfig('WMCore.WebTools.RESTModel')
        self.config.setDBUrl('sqlite://')
        self.schemaModules = ['WMCore.ThreadPool', 'WMCore.WMBS']
        """
        warnings.warn("You probably want to implement initialize()", Warning)

#!/usr/bin/env python2.6
"""
<testcase classname="WMCore_t.WMSpec_t.StdSpecs_t.MonteCarlo_t.MonteCarloTest" name="WMCore_t.WMSpec_t.StdSpecs_t.MonteCarlo_t.MonteCarloTest.testRelValMCWithPileup" time="0"><error type="DBSAPI.dbsApiException.DbsBadRequest">Traceback (most recent call last):
  File &quot;/jenkins/deploy/0.8.35/sw/slc5_amd64_gcc461/external/python/2.6.4-comp3/lib/python2.6/unittest.py&quot;, line 279, in run
    testMethod()
</error>

Looks at an xml file with the previous format and makes sure that nothing is failing that isn't in standards/allowed_failing_tests.txt
"""

import sys, os

testfile  = sys.argv[1]
whitelist = sys.argv[2]

from xml.dom.minidom import parse as parseXML

allowedErrors = []
fh = open(whitelist, 'r')
for line in fh.readlines():
    # remove annoying duplication nose does
    stripped = line.strip()
    splitted = stripped.split('.')
    for index in range(len(splitted) - 1):
        if splitted[0] == splitted[index + 1]:
            line = ".".join(splitted[index + 1:])
            break
    
    allowedErrors.append( line.strip() )    
fh.close()




def checkJunitFile( document, allowedErrors, keepAllowed = True, keepUnallowed = True, verbose = False):
    suitePasses = True
    # look at test suites
    for suite in document.childNodes:
        # look at testcases
        for case in suite.childNodes:
            if case.localName == 'testcase':
                for child in case.childNodes:
                    if child.localName in ['error', 'failure']:
                        if case.getAttribute('name') not in allowedErrors:
                            if verbose: print("Got an unallowed error: %s" % case.getAttribute('name'))
                            if not keepAllowed: 
                                case.removeChild( child )
                                child.unlink()
                                failType = child.localName + "s"
                                suite.setAttribute(failType, str(int(suite.getAttribute(failType)) - 1))
                            suitePasses = False
                        else:
                            if verbose: print("Got an allowed error (FIXME): %s" % case.getAttribute('name'))
                            if not keepUnallowed: 
                                case.removeChild( child )
                                child.unlink()
                                failType = child.localName + "s"
                                suite.setAttribute(failType, str(int(suite.getAttribute(failType)) - 1))
    return suitePasses

document      = parseXML( testfile )
suitePasses = checkJunitFile( document, allowedErrors, verbose = True)

ignoredErrors = document.cloneNode( True )
checkJunitFile( ignoredErrors, allowedErrors, keepUnallowed = False )
ignoredErrors.writexml( open('noseignored.xml','w') )
ignoredErrors.unlink()

trueErrors    = document.cloneNode( True )
checkJunitFile( trueErrors, allowedErrors, keepAllowed = False )
trueErrors.writexml( open('nosetrue.xml', 'w') )
trueErrors.unlink()

        
                        
if suitePasses:
    print "Suite is OK"
    sys.exit(0)
else:
    print "Suite FAILED"
    sys.exit(1)

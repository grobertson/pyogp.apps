# standard
import re
import getpass, sys, logging
from optparse import OptionParser
import uuid

# related
from eventlet import api

# pyogp
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings


def login():
    """ login an to a login endpoint """ 

    parser = OptionParser(usage="usage: %prog [options] firstname lastname")

    logger = logging.getLogger("client.example")

    parser.add_option("-l", "--loginuri", dest="loginuri", default="https://login.aditi.lindenlab.com/cgi-bin/login.cgi",
                      help="specified the target loginuri")
    parser.add_option("-r", "--region", dest="region", default=None,
                      help="specifies the region (regionname/x/y/z) to connect to")
    parser.add_option("-q", "--quiet", dest="verbose", default=True, action="store_false",
                    help="enable verbose mode")
    parser.add_option("-p", "--password", dest="password", default=None,
                      help="specifies password instead of being prompted for one")

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Expected arguments: firstname lastname")

    if options.verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG) # seems to be a no op, set it for the logger
        formatter = logging.Formatter('%(asctime)-30s%(name)-30s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        # setting the level for the handler above seems to be a no-op
        # it needs to be set for the logger, here the root logger
        # otherwise it is NOTSET(=0) which means to log nothing.
        logging.getLogger('').setLevel(logging.DEBUG)
    else:
        print "Attention: This script will print nothing if you use -q. So it might be boring to use it like that ;-)"

    # example from a pure agent perspective

    print "Attention: Creating a group will cost you 100 Lindens. Stop now if you don't like the sound of that."
    #grab a password!
    #grab a password!
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()

    # let's disable inventory handling for this example
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = False
    settings.ENABLE_OBJECT_TRACKING = False
    settings.ENABLE_COMMUNICATIONS_TRACKING = False
    settings.ENABLE_UDP_LOGGING =True
    settings.ENABLE_EQ_LOGGING = False
    settings.ENABLE_CAPS_LOGGING = True

    #First, initialize the agent
    client = Agent(settings = settings)

    # Now let's log it in
    api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location = options.region, connect_region = True)

    # wait for the agent to connect to it's region
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    # do sample script specific stuff here

    # use a random uuid for a good chance at having success with creating a group
    # Warning: this will cost you 100 Lindens
    group_name = str(uuid.uuid4())
    client.group_manager.create_group(Name = group_name.split('-')[4])

    while client.running:
        api.sleep(0)

    print ''
    print ''
    print 'At this point, we have an Agent object, Inventory dirs, and with a Region attribute'
    print 'Agent attributes:'
    for attr in client.__dict__:
        print attr, ':\t\t\t',  client.__dict__[attr]
    print ''
    print ''
    print 'Known Groups:'
    for group in client.group_manager.group_store:
        print ':\t\t\t',  group.GroupName

def main():
    return login()    

if __name__=="__main__":
    main()

"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0 (the "License").
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/LICENSE.txt

$/LicenseInfo$
"""


# standard
import re
import getpass, sys, logging
from optparse import OptionParser

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
                     help="specifies the region to connect to")
#http://ec2-75-101-203-98.compute-1.amazonaws.com:9000
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

   #grab a password!
   password = getpass.getpass()

   # let's disable inventory handling for this example
   settings = Settings()
   settings.ENABLE_INVENTORY_MANAGEMENT = False
   settings.ENABLE_EQ_LOGGING = False
   settings.ENABLE_CAPS_LOGGING = False

   #First, initialize the agent
   client = Agent(settings = settings)

   # Now let's log it in
   api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location = options.region, connect_region = True)

   # wait for the agent to connect to it's region
   while client.connected == False:
       api.sleep(0)

   while client.region.connected == False:
       api.sleep(0)

   # in this case, wait for the client.Position to become populated, as we need to rez a box
   # relative to our current position
   while client.Position == (0.0, 0.0, 0.0):
       api.sleep(10)

   # do sample script specific stuff here

   client.region.objects.create_default_box(GroupID = client.ActiveGroupID)

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
   print 'Objects being tracked: %s' % len(client.region.objects.object_store)
   print ''
   print ''
   states = {}
   for _object in client.region.objects.object_store:
       if _object.State != None:
           print 'LocalID:', _object.LocalID, '\tUUID: ', _object.FullID , '\tState: ', _object.State, '\tPosition: ', _object.Position
       else:
           if states.has_key(_object.State):
               states[_object.State]+=1
           else:
               states[_object.State] = 1
   print ''
   print 'Object states I don\'t care about atm'
   for state in states:
       print '\t State: ', state, '\tFrequency: ', states[state]
   print ''
   print ''
   print 'Avatars being tracked: %s' % len(client.region.objects.avatar_store)
   print ''
   print ''
   for _avatar in client.region.objects.avatar_store:
       print 'ID:', _avatar.LocalID, '\tUUID: ', _avatar.FullID , '\tNameValue: ', _avatar.NameValue, '\tPosition: ', _avatar.Position
   print ''
   print ''
   print 'Region attributes:'
   for attr in client.region.__dict__:
       print attr, ':\t\t\t',  client.region.__dict__[attr]

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


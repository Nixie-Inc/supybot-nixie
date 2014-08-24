###
# Copyright (c) 2014, Samir Faci
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.httpserver as httpserver
import supybot.ircmsgs as ircmsgs
import supybot.world as world
import re
import tinyurl as t


import feedparser
import threading
import random 



class Nixie(callbacks.Plugin):
    """Add the help for "@plugin help Nixie" here
    This should describe *how* to use this plugin."""
    nixiedocuments = None
    cached_nixiedocs = None


    def __init__(self, irc):
        self.rnd = random.Random()
        self.__parent = super(Nixie, self)
        self.__parent.__init__(irc)
        self.nixie_rss = "http://feeds.feedburner.com/nixiepixel"
        self.__create_nixiedocs()

    def __create_nixiedocs(self):
        self.nixiedocuments = {}
        self.nixiedocuments['BrainDump (unedited)'] = "https://docs.google.com/document/d/1Z6sOjoxhYXBoXydnI3ba8VWQys3T45Rd836TzNq6yZw/edit?usp=sharing"
        self.nixiedocuments['Community Plan'] = "https://docs.google.com/document/d/1TBQwaRhjDgFLi1xDmQfgY0OMyxhhUDLeKXZzv_NH_88/edit?usp=sharing"
        self.nixiedocuments['Linux Myths'] = "https://docs.google.com/document/d/1EF7D6iRLkVvK0NwRzp_KOOKABfqrJf0u023KBPRshts/edit?usp=sharing"
        self.nixiedocuments['Civic Involvement Brain Dump'] = "https://docs.google.com/document/d/1yGD1LK0fTnOLtor5xkIhZtTW02hqrgBkpMQqRU9OcF8/edit?usp=sharing"
        if self.cached_nixiedocs is None:
            self.cached_nixiedocs = {} 
            for key in self.nixiedocuments:
                self.cached_nixiedocs[key] = self._tinyurl(self.nixiedocuments[key]) 
 


    def _tinyurl(self, url):
        return t.create_one(url)

    def nixiecontact(self, irc, msg, args):
        """
          Returns the nixiecontact information
        """

        irc.reply("Twitter:  twitter.com/nixiepixel", private=True)
        irc.reply("Facebook: http://fb.me/nixiepixel", private=True)
        irc.reply("Google+: http://google.me/+NixiePixel", private=True)
        irc.reply("Patreon: http://patreon.com/nixiepixel", private=True)
        irc.reply("Steam group: http://steamcommunity.com/groups/nixiepixel", private=True)
    nixiecontact = wrap(nixiecontact)


    def nixiedocs(self, irc, msg, args):
        """
          Returns the set of collaborative documents created by the community.
        """          
        [ irc.reply(key + ": " + self.cached_nixiedocs[key], private=True) for key in self.cached_nixiedocs]
        irc.reply("Github 'cause why note: https://github.com/Nixie-Inc/FOSSCommunity/wiki", private=True)
    nixiedocs = wrap(nixiedocs)
  
    #TODO: make this less.. sucky 
    def nixierandom(self, irc, msg, args, channel):
        """
          select a random user from current room
        """
        chanObj = irc.state.channels[channel]
        users = chanObj.users
        arrayUser = []
        for user in users:
            arrayUser.append(user)
        ndx = self.rnd.randint(0, len(users))
        irc.reply(arrayUser[ndx])
    nixierandom  = wrap(nixierandom, ['channel'] )

    def nixiefeed(self, irc, msg, args):
        """
        returns top 5 entires of nixie's website RSS feed.

        """
        print args
        feed = feedparser.parse(self.nixie_rss)
        items = feed['entries'][:5]
        [ irc.reply(item['published'] + ":  " + item['title'] + " ::: " + item['id'], private=True) for item in items]  
    nixiefeed  = wrap(nixiefeed)

Class = Nixie



# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

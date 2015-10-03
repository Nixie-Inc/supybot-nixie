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
import supybot.ircdb as ircdb
import re
import tinyurl as t
import subprocess as proc
from pyfiglet import figlet_format


import feedparser
import threading
import random 



class Nixie(callbacks.Plugin):
    """Add the help for "@plugin help Nixie" here
    This should describe *how* to use this plugin."""
    nixiedocuments = None
    cached_nixiedocs = None


    def __init__(self, irc):
        self.__parent = super(Nixie, self)
        self.__parent.__init__(irc)
        self.rnd = random.SystemRandom() 
        self.nixie_rss = "http://feeds.feedburner.com/nixiepixel"
        self.excludes = set(['nixie', 'ChanServ', 'llama-bot', 'Yami-no-Ryama'])

    def _tinyurl(self, url):
        return t.create_one(url)

    def admintest(self, irc, msg, args):
        """
          Checks to see if user is an Admin
        """
        if  not  ircdb.checkCapability(msg.prefix, 'admin'):
            irc.reply("DENIED! Not an OP")
            return
        irc.reply("Hello Master")

    admintest = wrap(admintest)


    def banner(self, irc, msg, args, text):
        """
          Returns the text passed in as a 'banner' to annoy everyone with.
        """
        if  not  ircdb.checkCapability(msg.prefix, 'admin'):
            self.log.warning("Permission Denied!")
            return
        resp = figlet_format(text, font='banner')
        lines = resp.split("\n")
        for line in lines:
            if len(line) == 0:
                continue
            irc.reply(line)

    banner = wrap(banner, ['text'])

    def rules(self, irc, msg, args):
        """
          Returns rules of the channel
        """

        irc.reply("""These rules should really be self evident.  Don't be an ass, be courteous, don't make the ops take out the ban hammer.  We really don't want to be paying that close attention to the room.  If you make us police you you'll get a firm kick in the tush.  In other words...  read this: http://www.ubuntu.com/about/about-ubuntu/conduct it's a good guideline of what to do / not do""", private=False)

    rules = wrap(rules)


    def nixiecontact(self, irc, msg, args):
        """
          Returns the nixiecontact information
        """

        irc.reply("Contact Info Page: http://www.osalt.tech/contact/nixie", private=True)

    nixiecontact = wrap(nixiecontact)

    def _sendMsg(self, irc, msg):
        irc.queueMsg(msg)
        irc.noReply()

    def smackroom(self, irc, msg, args, channel):
        """
           bitch slap everyone in the room.
        """
        if  not  ircdb.checkCapability(msg.prefix, 'admin'):
            irc.reply("Permission Denied!")
            return

        chanObj = irc.state.channels[channel]
        users = chanObj.users
        for user in users:
            if user in self.excludes:
                continue
            irc.reply("slaps {user} with a big wet trout".format(user=user))
    smackroom  = wrap(smackroom, ['channel'] )



    def hugroom(self, irc, msg, args, channel):
        """
           hugs everyone in the room.
        """
        if  not  ircdb.checkCapability(msg.prefix, 'admin'):
            irc.reply("Permission Denied!")
            return

        chanObj = irc.state.channels[channel]
        users = chanObj.users
        for user in users:
            if user in self.excludes:
                continue
            irc.reply("huggles {user}".format(user=user))
    hugroom  = wrap(hugroom, ['channel'] )

    def nixietime(self, irc, msg, args, channel):
        """
          returns the definition of f(nixietime)
        """
        message = """ F(NixieTime) is defined as a function of F that represents the current time plus a nondeterministic random value denoting a temporal period.  The exact value of the delta is unknown and changes constantly based on fluctuation in the space time continuum and doctor who paradoxes  """
        irc.reply(message)
    nixietime  = wrap(nixietime, ['channel'] )

  
    def nixierandom(self, irc, msg, args, channel):
        """
          select a random user from current room
        """
        chanObj = irc.state.channels[channel]
        users = chanObj.users
        array_users = []
        for user in users:
            if user in self.excludes:
                continue
            array_users.append(user)
        irc.reply(self.rnd.choice(array_users))
    nixierandom  = wrap(nixierandom, ['channel'] )

    def llamaride(self, irc, msg, args, channel):
        """
          Go for a Llama ride
        """
        irc.reply("yeeeeeeeeeeehhhhhaaaa, yippee ki yay")
    llamaride  = wrap(llamaride, ['channel'] )

    def questions(self, irc, msg, args, channel):
        """
          Displays the link where to post your questions.
        """
        irc.reply("Visit:  http://goo.gl/aQDVu0 to submit your questions.")
    questions  = wrap(questions, ['channel'] )


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

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


    def nixiecontact(self, irc, msg, args):
        """
          Returns the nixiecontact information
        """

        irc.reply("Contact Info Page: http://osalt.github.io/pages/contact.html", private=True)

    nixiecontact = wrap(nixiecontact)


    def nixiedocs(self, irc, msg, args):
        """
          Returns the set of collaborative documents created by the community.
        """          
        irc.reply("http://osalt.github.io/pages/community-planning.html", private=True)
    nixiedocs = wrap(nixiedocs)

    def _sendMsg(self, irc, msg):
        irc.queueMsg(msg)
        irc.noReply()

    #def spin(self, irc, msg, args, channel):
    #    """
    #      select a random user from current room
    #    """
    #    if  not  ircdb.checkCapability(msg.prefix, 'admin') and name.lower() =="nixie":
    #        irc.reply("Permission Denied!")
    #        return
    #    chanObj = irc.state.channels[channel]
    #    users = chanObj.users
    #    array_users = []
    #    for user in users:
    #        if user in self.excludes:
    #            continue
    #        array_users.append(user)
    #    #irc.reply("kicking:" + self.rnd.choice(array_users))
    #    #sheep = self.rnd.choice(array_users)
    #    sheep = 'csgeek'
    #    irc.reply("trying to kick:" + sheep)
    #    print (dir(irc))
    #    ircmsgs.kick(channel, sheep)
    #    self._sendMsg(irc, ircmsgs.kick(channel, sheep, "bye bye"))
    #spin  = wrap(spin, ['channel'] )


  
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


    def ces(self, irc, msg, args, channel):
        """
          Form to submit questions / comments about CES coverage.
        """
        irc.reply("Submit CES related questions here: http://osalt.github.io/pages/forms.html")
    ces = wrap(ces, ['channel'] )


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


    def listquestions(self, irc, msg, args, channel):
        """
        This method will list the top 10 questions in the queue
        """
        irc.reply("This opperation is currently unsupported")
    listquestions  = wrap(listquestions, ['channel'] )


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

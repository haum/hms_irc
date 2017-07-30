"""Receiver that will print out every mention of the Mastodon account."""


def handle(irc_server, irc_chan, dct):

    def irc(msg):
        irc_server.privmsg(irc_chan, msg)

    irc('[Mastodon] ' + dct['user'] + ' « ' + dct['text_content'] + ' » ' +
        dct['url'])

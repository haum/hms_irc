"""Sends a toot to the HAUM's Mastodon account."""

import logging

from hms_irc import strings
from hms_irc.irc import IRCHandler


def get_logger():
    return logging.getLogger(__name__)


class TootHandler(IRCHandler):
    def handle(self, command):
        get_logger().info('Toot with command {}'.format(command))

        # TODO: Ugly way of testing command arguments...
        if command.command_args and command.command_args[0]:
            if command.is_voiced:
                self.toot(' '.join(command.command_args))
                self.chanmsg(strings.TOOT_PENDING)
        else:
            self.display_usage()

    def display_usage(self):
        self.chanmsg(strings.TOOT_USAGE)

    def toot(self, msg):
        """Closure for sending a toot."""
        self.rabbit.publish(
            'mastodon.toot', {
                'message': msg,
                'source': 'irc'
            })


def handle(irc_server, irc_chan, rabbit, command):
    h = TootHandler(irc_server, irc_chan, rabbit)
    h.handle(command)

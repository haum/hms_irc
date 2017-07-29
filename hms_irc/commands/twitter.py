"""Sends a tweet to Twitter using the HAUM account."""

import logging

from hms_irc import strings
from hms_irc.irc import IRCHandler


def get_logger():
    return logging.getLogger(__name__)


class TwitterHandler(IRCHandler):
    def handle(self, command):
        get_logger().info('Tweet with command {}'.format(command))

        # TODO: Ugly way of testing command arguments...
        if command.command_args and command.command_args[0]:
            if command.is_voiced:
                if command.command_args[0] == 'tweet':
                    self.tweet(' '.join(command.command_args[1:]))
                    self.chanmsg(strings.TWEET_PENDING)
        else:
            self.display_usage()

    def display_usage(self):
        self.chanmsg(strings.TWEET_USAGE)

    def tweet(self, msg):
        """Closure for sending a tweet."""
        self.rabbit.publish(
            'twitter.query', {
                'command': 'tweet',
                'status': msg,
                'source': 'irc'
            })


def handle(irc_server, irc_chan, rabbit, command):
    h = TwitterHandler(irc_server, irc_chan, rabbit)
    h.handle(command)

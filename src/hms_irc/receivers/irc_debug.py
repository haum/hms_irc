"""Receives debug messages and print them directly into the IRC chan."""

import logging


def get_logger():
    return logging.getLogger(__name__)


def msg_to_privmsg(msg):
    """Extract the PRIVMSG content from the RabbitMQ message."""
    if 'privmsg' in msg:
        return msg['privmsg']

    return None


def handle(irc_server, irc_chan, msg):

    privmsg = msg_to_privmsg(msg)

    if privmsg is not None:
        irc_server.privmsg(irc_chan, privmsg)
        get_logger().info('Posted irc_debug message: {}'.format(privmsg))
    else:
        get_logger().warning('Received irc_debug message without privmsg '
                             'field. Aborting.')

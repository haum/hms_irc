"""Prints out new reddit submissions.

The title, url and username of the submission will be printed in the IRC chan.

"""

import logging


def get_logger():
    return logging.getLogger(__name__)


def msg_to_privmsg(msg):
    """Extract the PRIVMSG content from the RabbitMQ message."""
    return '[reddit /u/{author}] {title} {url}'.format(**msg)


def handle(irc_server, irc_chan, msg):
    irc_server.privmsg(irc_chan, msg_to_privmsg(msg))
    get_logger().info('Posted reddit link {id} from {author}'.format(**msg))

import logging

from hms_irc import strings


def get_logger():
    return logging.getLogger(__name__)


def handle(irc_server, irc_chan, rabbit, command):

    # Define some useful closures

    def toot(message):
        """Closure for sending a toot."""
        rabbit.publish(
            'mastodon.toot', {
                'message': message,
                'source': 'irc'
            })

    def chanmsg(msg):
        """Closure for sending a privmsg on the chan."""
        irc_server.privmsg(irc_chan, msg)

    get_logger().info('Toot with command {}'.format(command))

    # TODO: Ugly way of testing command arguments...
    if command.command_args and command.command_args[0]:
        if command.is_voiced:
            toot(' '.join(command.command_args))
            chanmsg(strings.TOOT_PENDING)
    else:
        chanmsg(strings.TOOT_USAGE)
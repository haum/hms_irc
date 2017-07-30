import importlib
import logging
import signal

import irc.bot
from irc.client import NickMask, ServerConnectionError

from hms_irc.irc import IRCCommand


def get_logger():
    return logging.getLogger(__name__)


class MyBot(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667):
        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        self.joined = False
        self.serv = None
        self.join_callback = None
        self.rabbit = None

        # try to reconnect whenever a SIGUSR1 is received
        signal.signal(signal.SIGUSR1, self.handle_reconnection_request)

    def on_welcome(self, serv, ev):
        """Method called when we are connected to the IRC server."""
        self.serv = serv
        get_logger().info("Signed on")
        get_logger().info("Joining {}...".format(self.channel))
        serv.join(self.channel)

    def on_join(self, serv, ev):
        """Method called when we join an IRC chan."""
        self.joined = True
        get_logger().info("Joined {}".format(self.channel))

        if self.join_callback is not None:
            self.join_callback()

    def on_kick(self, serv, ev):
        """Method called when someone was kicked on a chan."""
        get_logger().warning("An user has been kicked")

    def on_nicknameinuse(self, serv, ev):
        """Method called when the nickname is already in use."""
        newnick = serv.get_nickname() + '_'
        get_logger().warning("Nick already in use, using {}".format(newnick))
        serv.nick(newnick)

    def on_privmsg(self, serv, ev):
        """Method called when someone is talking in private to us."""
        get_logger().info("PRIVMSG {}".format(ev))
        serv.privmsg(NickMask(ev.source).nick, "hey")

    def on_pubmsg(self, serv, ev):
        """Method called when someone is talking on a public chan."""
        message = ev.arguments[0]
        nick = NickMask(ev.source).nick

        if message.startswith('!'):
            # Extract command from message
            command_text = message[1:]
            command_parts = command_text.split(' ')

            command = IRCCommand(
                nick=nick,
                is_voiced=self.channels[self.channel].is_voiced(nick),
                command_name=command_parts[0].lower(),
                command_args=command_parts[1:]
            )

            get_logger().info("Received {}".format(command))

            # Handle special case for spacestatus (path dependency...)
            if command.command_name.startswith('space'):
                command.command_name = 'spacestatus'

            try:
                # Retrieve the 'handle' function from corresponding module
                module = importlib.import_module(
                    'hms_irc.commands.{}'.format(command.command_name))
                func = getattr(module, 'handle')

                # Call the handle function with all important arguments
                get_logger().info('Calling transmitter for {}'.format(command))
                func(self.serv, self.channel, self.rabbit, command)

            except (ImportError, AttributeError) as e:
                get_logger().error(e)
                self.serv.privmsg(self.channel, 'Commande inexistante')

    def on_disconnect(self, serv, ev):
        """Method called when we disconnect from the IRC server."""
        get_logger().info("Disconnected")

    def handle_rabbit_msg(self, client, topic, dct):
        """Method that will handle incoming RabbitMQ messages."""

        get_logger().info('Handle rabbit msg topic {}'.format(topic))
        try:
            module = importlib.import_module('hms_irc.receivers.' + topic)
            func = getattr(module, 'handle')

            get_logger().info('Calling handler for topic {}'.format(topic))

            func(self.serv, self.channel, dct)

        except (ImportError, AttributeError) as e:
            get_logger().error(e)

    def handle_reconnection_request(self, signum, frame):
        """Method forcing a reconnection attempt.

        This is used when the bot's PID receives a particular
        signal. Useful to handle *.net *.split. Silent if still connected."""
        self.reconnect_if_disconnected(force_reconnect=True)

    def reconnect_if_disconnected(self, force_reconnect=False):
        if not self.serv:
            get_logger().error('Reconnection request received but no serv is'
                               ' currently set. Ignoring.')
            return

        try:
            get_logger().info(
                'Reconnection request received, processing...')

            if self.serv.connected and not force_reconnect:
                get_logger().info('Server already connected, nothing to do')
            else:
                get_logger().info('Reconnecting')
                self.serv.reconnect()

        except ServerConnectionError as e:
            get_logger().error(e)

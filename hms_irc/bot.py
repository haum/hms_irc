import logging
import json
import importlib

import irc.bot
from irc.client import NickMask

from hms_irc import settings


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

    def on_welcome(self, serv, ev):
        """Method called when we are connected to the IRC server."""
        self.serv = serv
        get_logger().info("Signed on")
        get_logger().info("Joining {}...".format(self.channel))
        serv.join(self.channel)

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
        self.serv.privmsg(NickMask(ev.source).nick, "hey")

    def on_pubmsg(self, serv, ev):
        """Method called when someone is talking on a public chan."""
        message = ev.arguments[0]

        if message.startswith('!'):
            command_text = message[1:]
            command_parts = command_text.split(' ')
            command_name = command_parts[0]
            command_args = command_parts[1:]

            get_logger().info("Received command {} with args {}"
                              .format(command_name, command_args))

            data = {
                'command': command_name,
                'arg': ' '.join(command_args),
                'nick': NickMask(ev.source).nick
            }

            self.rabbit.publish(settings.RABBIT_COMMAND_ROUTING_KEY, data)

    def on_join(self, serv, ev):
        """Method called when we join an IRC chan."""
        self.joined = True
        get_logger().info("Joined {}".format(self.channel))

        if self.join_callback is not None:
            self.join_callback()

    def on_disconnect(self, serv, ev):
        """Method called when we disconnect from the IRC server."""
        get_logger().info("Disconnected")

    def handle_rabbit_msg(self, client, topic, dct):
        """Method that will handle incoming RabbitMQ messages."""

        try:
            module = importlib.import_module('hms_irc.handlers.' + topic)
            func = getattr(module, 'handle')

            get_logger().info('Calling handler for topic {}'.format(topic))

            func(self.serv, self.channel, dct)

        except (ImportError, AttributeError) as e:
            get_logger().error(e)

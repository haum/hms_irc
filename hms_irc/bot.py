import logging

import irc.bot


def get_logger():
    return logging.getLogger(__name__)


class MyBot(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667):
        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        self.joined = False
        self.serv = None

    def on_welcome(self, serv, ev):
        self.serv = serv
        get_logger().info("Signed on")
        get_logger().info("Joining {}".format(self.channel))
        serv.join(self.channel)

    def on_kick(self, serv, ev):
        get_logger().warning("Kicked")
        self.die('got kicked')

    def on_nicknameinuse(self, serv, ev):
        newnick = serv.get_nickname() + '_'
        get_logger().warning("Nick already in use, using {}".format(newnick))
        serv.nick(newnick)

    def on_join(self, serv, ev):
        self.joined = True
        get_logger().info("Joined {}".format(self.channel))

    def rabbit(self, ch, method, properties, body):
        self.serv.privmsg(self.channel, body)

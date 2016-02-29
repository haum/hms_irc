import sys
import logging
import json

import irc.bot


def get_logger():
    return logging.getLogger(__name__)


class MyBot(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667):
        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        self.joined = False
        self.serv = None
        self.join_callback = None

    def on_welcome(self, serv, ev):
        self.serv = serv
        get_logger().info("Signed on")
        get_logger().info("Joining {}...".format(self.channel))
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

        if self.join_callback is not None:
            self.join_callback()

    def on_disconnect(self, serv, ev):
        get_logger().info("Goodbye")
        sys.exit(0)

    def rabbit(self, ch, method, properties, body):

        if method.routing_key == 'reddit':
            item = json.loads(body.decode('utf-8'))

            msg = '[reddit /u/{}] {} {}'.format(
                item['author'], item['title'], item['url'])

            self.serv.privmsg(self.channel, msg)

            get_logger().info('Posted reddit link {} from {}'.format(
                item['id'], item['author']))

        else:
            get_logger().warning(
                'Message from routing key {} not handled'.format(
                    method.routing_key))

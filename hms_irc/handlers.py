import logging


def get_logger():
    return logging.getLogger(__name__)


def reddit(irc_server, irc_chan, msg):

    privmsg = '[reddit /u/{}] {} {}'.format(
        msg['author'], msg['title'], msg['url'])

    irc_server.privmsg(irc_chan, privmsg)

    get_logger().info('Posted reddit link {} from {}'.format(
        msg['id'], msg['author']))

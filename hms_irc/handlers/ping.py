import logging


def get_logger():
    return logging.getLogger(__name__)


def handle(irc_server, irc_chan, msg):

    if msg['type'] == 'request' and msg['source'] == 'irc':

        privmsg = ('Ping envoyé. All your microservices are belong to '
                   'us.'.format(msg))

        irc_server.privmsg(irc_chan, privmsg)
        get_logger().info('Posted ping message: {}'.format(privmsg))

    elif msg['type'] == 'answer' and msg['source']['source'] == 'irc':

        privmsg = 'Le service `{}` a répondu présent'.format(msg['name'])

        irc_server.privmsg(irc_chan, privmsg)
        get_logger().info('Posted pong message: {}'.format(privmsg))

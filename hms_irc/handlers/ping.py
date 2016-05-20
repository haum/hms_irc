import logging


def get_logger():
    return logging.getLogger(__name__)


def handle(irc_server, irc_chan, msg):

    if msg['type'] == 'request':

        privmsg = 'Une requêtre globale de ping a été envoyée {}'.format(msg)

        irc_server.privmsg(irc_chan, privmsg)
        get_logger().info('Posted ping message: {}'.format(privmsg))

    elif msg['type'] == 'answer':

        privmsg = 'Réponse reçue au ping {}'.format(msg)

        irc_server.privmsg(irc_chan, privmsg)
        get_logger().info('Posted pong message: {}'.format(privmsg))

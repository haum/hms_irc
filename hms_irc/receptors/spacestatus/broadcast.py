import logging


def get_logger():
    return logging.getLogger(__name__)


def dct_to_privmsg(dct):
    is_open = dct['is_open']

    if is_open:
        return 'BROADCAST L’espace est ouvert !'
    else:
        return 'BROADCAST L’espace est fermé !'


def handle(irc_server, irc_chan, dct):
    irc_server.privmsg(irc_chan, dct_to_privmsg(dct))
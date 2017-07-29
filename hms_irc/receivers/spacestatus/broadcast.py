"""Receiver that prints out broadcasted openings and closings of the space.

.. todo::

    This receiver will also print out commands for twaum (perl twitter bot)
    to indicate the status on twitter. This should be removed and commands
    should be sent to hms_twitter.

"""

import logging

from hms_irc import strings


def get_logger():
    return logging.getLogger(__name__)


def dct_to_privmsg(dct):
    is_open = dct['is_open']

    if is_open:
        return 'BROADCAST L’espace est ouvert !'
    else:
        return 'BROADCAST L’espace est fermé !'


def dct_to_twaum(dct):
    is_open = dct['is_open']

    if is_open:
        return strings.TWAUM_OPEN
    else:
        return strings.TWAUM_CLOSED


def handle(irc_server, irc_chan, dct):
    # irc_server.privmsg(irc_chan, dct_to_privmsg(dct))
    irc_server.privmsg(irc_chan, dct_to_twaum(dct))

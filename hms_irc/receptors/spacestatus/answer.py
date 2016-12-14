import logging
from hms_irc import strings


def get_logger():
    return logging.getLogger(__name__)


def dct_to_privmsg(dct):
    is_open = dct['is_open']

    has_changed = dct['has_changed'] if 'has_changed' in dct else True

    msg = strings.SPACESTATUS_OPEN if is_open else strings.SPACESTATUS_CLOSED

    # Check if state changed or not
    if not has_changed:
        msg += strings.SPACESTATUS_SAME_STATE

    return msg


def handle(irc_server, irc_chan, dct):
    irc_server.privmsg(irc_chan, dct_to_privmsg(dct))
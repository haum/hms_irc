"""Receiver used when the spacestatus service answers user requests."""

import logging
from hms_irc import strings


def get_logger():
    return logging.getLogger(__name__)


def handle(irc_server, irc_chan, dct):
    is_open = dct['is_open']
    has_changed = dct['has_changed'] if 'has_changed' in dct else True

    # Space status info (open or closed)
    msg = strings.SPACESTATUS_OPEN if is_open else strings.SPACESTATUS_CLOSED

    # Check if state changed or not
    if not has_changed:
        msg += strings.SPACESTATUS_SAME_STATE

    irc_server.privmsg(irc_chan, msg)

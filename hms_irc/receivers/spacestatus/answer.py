"""Receiver used when the spacestatus service answers user requests."""

import logging
from hms_irc import strings


def get_logger():
    return logging.getLogger(__name__)


def dct_to_privmsgs(dct):
    is_open = dct['is_open']
    has_changed = dct['has_changed'] if 'has_changed' in dct else True

    # Space status info (open or closed)
    line1 = strings.SPACESTATUS_OPEN if is_open else strings.SPACESTATUS_CLOSED

    # Check if state changed or not
    if not has_changed:
        line1 += strings.SPACESTATUS_SAME_STATE

    # On line 2 we want to know SpaceApi response
    if 'spaceapi' in dct:
        spaceapi = dct['spaceapi']

        def check(x):
            return x in spaceapi and spaceapi[x]

        line2 = '[SpaceAPI] '

        if check('is_open'):
            line2 += strings.SPACEAPI_OPEN
        else:
            line2 += strings.SPACEAPI_CLOSED

        if check('ssl_error'):
            line2 += ' ({})'.format(strings.SPACEAPI_BAD_SSL)
        if check('bad_http_code'):
            line2 += ' ({})'.format(strings.SPACEAPI_BAD_HTTP_CODE)
        if check('global_error'):
            line2 += ' ({})'.format(strings.SPACEAPI_GLOBAL_ERROR)

        return (line1, line2)

    return (line1,)


def handle(irc_server, irc_chan, dct):
    for msg in dct_to_privmsgs(dct):
        irc_server.privmsg(irc_chan, msg)

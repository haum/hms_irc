import logging
from hms_irc import strings


def get_logger():
    return logging.getLogger(__name__)


def dct_to_privmsgs(dct):
    is_open = dct['is_open']
    has_changed = dct['has_changed'] if 'has_changed' in dct else True

    # Space status info (open or closed)
    line1 = strings.SPACESTATUS_OPEN if is_open else strings.SPACESTATUS_CLOSED

    # Check if state changed or not
    if not has_changed:
        line1 += strings.SPACESTATUS_SAME_STATE

    # On line 2 we want to know SpaceApi response
    spaceapi_open = dct['spaceapi']['is_open']
    spaceapi_badssl = dct['spaceapi']['ssl_error']
    spaceapi_badhttp = dct['spaceapi']['bad_http_code']
    spaceapi_globalerror = dct['spaceapi']['global_error']

    line2 = '[SpaceAPI] '
    line2 += strings.SPACEAPI_OPEN if spaceapi_open else strings.SPACEAPI_CLOSED

    if spaceapi_badssl:
        line2 += ' ({})'.format(strings.SPACEAPI_BAD_SSL)
    if spaceapi_badhttp:
        line2 += ' ({})'.format(strings.SPACEAPI_BAD_HTTP_CODE)
    if spaceapi_globalerror:
        line2 += ' ({})'.format(strings.SPACEAPI_GLOBAL_ERROR)

    return (line1, line2)


def handle(irc_server, irc_chan, dct):
    for msg in dct_to_privmsgs(dct):
        irc_server.privmsg(irc_chan, msg)
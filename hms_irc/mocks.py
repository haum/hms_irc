from unittest.mock import Mock


def rabbit_mock():
    """Builds a rabbit mock and returns it."""
    rabbit = Mock()
    rabbit.publish = Mock()
    return rabbit


def irc_server_mock():
    """Builds an irc server mock and returns it."""
    irc_server = Mock()
    irc_server.privmsg = Mock()
    return irc_server
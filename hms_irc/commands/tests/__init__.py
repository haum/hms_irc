from unittest.mock import Mock

from hms_irc.irc import IRCCommand


class CommandBuilder:

    def __init__(self):
        self.is_voiced = False
        self.command_args = ""

    def voiced(self):
        self.is_voiced = True
        return self

    def args(self, args):
        self.command_args = args
        return self

    def build(self):
        splitted_args = None
        if self.command_args != "":
            splitted_args = self.command_args.split(' ')

        return IRCCommand(
            nick="toto",
            is_voiced=self.is_voiced,
            command_name="spacestatus",
            command_args=splitted_args)


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
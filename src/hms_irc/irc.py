import attr

from hms_irc import strings


class NotVoicedError(Exception):
    """Raised when user call a command but is not voiced"""
    pass


@attr.s
class IRCCommand:
    nick = attr.ib()
    is_voiced = attr.ib()
    command_name = attr.ib()
    command_args = attr.ib()


@attr.s
class IRCHandler:
    """Base IRC handler.

    One must reimplement the ``handle`` method in order to handle commands.

    """
    irc_server = attr.ib()
    irc_chan = attr.ib()
    rabbit = attr.ib()

    def chanmsg(self, msg):
        """Sends a privmsg on the chan."""
        self.irc_server.privmsg(self.irc_chan, msg)

    def handle(self, command):
        raise NotImplementedError


class SubcommandIRCHandler(IRCHandler):
    """Subcommand-based IRC handler.

    Can handle multiple subcommands easily using introspection.
    For example the ``!myhandler add`` will call ``handler.cmd_add`` and
    ``!myhandler delete`` will call ``handler.cmd_delete``.

    """

    def handle(self, command):
        """Automatic handler, routing to dedicated methods for subcommands."""
        if not command.command_args:
            return self.without_subcommand()

        subcommand = command.command_args[0]
        try:
            subcommand_handler = getattr(self, "cmd_{}".format(subcommand))
        except AttributeError:
            return self.subcommand_not_found(command)
        else:
            try:
                return subcommand_handler(command)
            except NotVoicedError:
                self.not_voiced(command)

    def without_subcommand(self):
        """Called when no subcommand has been provided.

        For example, !myhandler will call this method because no subcommand
        is provided.

        """
        raise NotImplementedError

    def subcommand_not_found(self, command):
        """Called when the provided subcommand was not found."""
        raise NotImplementedError

    def not_voiced(self, command):
        self.chanmsg(strings.MUST_BE_VOICED)


def voiced(handler):
    def verify_voiced(instance, command):
        if not command.is_voiced:
            raise NotVoicedError

        handler(instance, command)
    return verify_voiced

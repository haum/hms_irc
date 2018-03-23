import attr

from hms_irc import strings, settings
from hms_irc.irc.exceptions import NotVoicedError


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


class CompatIRCHandler(IRCHandler):
    """Compatibility handler for commands that are not migrated yet."""

    def handle(self, command):
        data = {
            'command': command.command_name,
            'arg': ' '.join(command.command_args),
            'nick': command.nick,
            'is_voiced': command.is_voiced
        }

        self.rabbit.publish(settings.RABBIT_COMMAND_ROUTING_KEY, data)


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

    def subcommand_not_found(self, subcommand):
        """Called when the provided subcommand was not found."""
        raise NotImplementedError

    def not_voiced(self, command):
        self.chanmsg(strings.MUST_BE_VOICED)

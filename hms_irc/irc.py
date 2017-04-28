import attr


@attr.s
class IRCCommand:
    nick = attr.ib()
    is_voiced = attr.ib()
    command_name = attr.ib()
    command_args = attr.ib()


@attr.s
class IRCHandler:
    irc_server = attr.ib()
    irc_chan = attr.ib()
    rabbit = attr.ib()

    def chanmsg(self, msg):
        """Sends a privmsg on the chan."""
        self.irc_server.privmsg(self.irc_chan, msg)

    def handle(self, command):
        raise NotImplementedError
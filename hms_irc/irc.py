import attr


@attr.s
class IRCCommand:
    nick = attr.ib()
    is_voiced = attr.ib()
    command_name = attr.ib()
    command_args = attr.ib()
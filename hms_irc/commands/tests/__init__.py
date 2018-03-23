from hms_irc.irc.commands import IRCCommand


def build_command(command, nick="toto", voiced=False):
    split_command = command.split(' ')
    return IRCCommand(
        nick=nick,
        is_voiced=voiced,
        command_name=split_command[0],
        command_args=split_command[1:])

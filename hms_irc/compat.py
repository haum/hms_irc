from hms_irc import settings


def handle(irc_server, irc_chan, rabbit, command):

    data = {
        'command': command.command_name,
        'arg': ' '.join(command.command_args),
        'nick': command.nick,
        'is_voiced': command.is_voiced
    }

    rabbit.publish(settings.RABBIT_COMMAND_ROUTING_KEY, data)
from hms_irc import strings


VOICED_ARGUMENTS = ['open', 'close', 'open_silent', 'close_silent']
VALID_ARGUMENTS = VOICED_ARGUMENTS + ['help']


def handle(irc_server, irc_chan, rabbit, command):
    # A simple closure for query
    query = lambda command: rabbit.publish(
        'spacestatus.query', {
            'command': command,
            'source': 'irc'
        })

    # A simple closure for privmsg on the chan
    chanmsg = lambda msg: irc_server.privmsg(irc_chan, msg)

    # A simple closure for help
    help = lambda: chanmsg(strings.SPACESTATUS_HELP.format(VALID_ARGUMENTS))

    # No argument provided
    if not command.command_args:
        query('status')
        return

    else:
        # Check argument user provided
        argument = command.command_args[0]
        if argument not in VALID_ARGUMENTS:
            chanmsg(strings.UNKNOWN_ARGUMENT)
            help()
            return

        # Check if command needs to be voiced
        if argument in VOICED_ARGUMENTS and not command.is_voiced:
            chanmsg(strings.MUST_BE_VOICED)
            return

        # Handle help
        if argument == 'help':
            help()

        # The argument is correct, send it to the spacestatus microservice
        query(argument)
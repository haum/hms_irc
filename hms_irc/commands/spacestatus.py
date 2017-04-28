from hms_irc import strings

VOICED_ARGUMENTS = ['open', 'close', 'open_silent', 'close_silent']
VALID_ARGUMENTS = VOICED_ARGUMENTS + ['help']


def handle(irc_server, irc_chan, rabbit, command):

    # Define some useful closures

    def query(command):
        """Closure for sending a query to the spacestatus microservice."""
        rabbit.publish(
            'spacestatus.query', {
                'command': command,
                'source': 'irc'
            })

    def chanmsg(msg):
        """Closure for sending a privmsg on the chan."""
        irc_server.privmsg(irc_chan, msg)

    def help():
        """Closure for displaying help."""
        chanmsg(strings.SPACESTATUS_HELP.format(VALID_ARGUMENTS))

    # If no argument provided, just check current status
    if not command.command_args:
        query('status')
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

        # If help required just display it and do not send query
        if argument == 'help':
            help()
            return

        # The argument is correct, send it to the spacestatus microservice
        query(argument)

"""Requests status change for the physical hackerspace location."""

from hms_irc import strings
from hms_irc.irc.handlers import IRCHandler


VOICED_ARGUMENTS = ['open', 'close', 'open_silent', 'close_silent', 'toggle',
                    'toggle_silent']
VALID_ARGUMENTS = VOICED_ARGUMENTS + ['help']


class SpaceStatusHandler(IRCHandler):

    def handle(self, command):
        # If no argument provided, just check current status
        if not command.command_args:
            self.query('status')
        else:
            # Check argument user provided
            argument = command.command_args[0]
            if argument not in VALID_ARGUMENTS:
                self.chanmsg(strings.UNKNOWN_ARGUMENT)
                self.display_help()
                return

            # Check if command needs to be voiced
            if argument in VOICED_ARGUMENTS and not command.is_voiced:
                self.chanmsg(strings.MUST_BE_VOICED)
                return

            # If help required just display it and do not send query
            if argument == 'help':
                self.display_help()
                return

            # The argument is correct, send it to the spacestatus microservice
            self.query(argument)

    def query(self, command):
        """Sends query to the spacestatus microservice."""
        self.rabbit.publish(
            'spacestatus.query', {
                'command': command,
                'source': 'irc'
            })

    def display_help(self):
        """Shows help to the user in the chan."""
        self.chanmsg(strings.SPACESTATUS_HELP.format(VALID_ARGUMENTS))


def handle(irc_server, irc_chan, rabbit, command):
    h = SpaceStatusHandler(irc_server, irc_chan, rabbit)
    h.handle(command)

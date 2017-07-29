"""Handle agenda events with read and write access."""

import re

from hms_irc import strings
from hms_irc.irc import IRCHandler


VOICED_ARGUMENTS = ['add', 'add_seance', 'remove', 'modify']
VALID_ARGUMENTS = VOICED_ARGUMENTS + ['help', 'all']


class AgendaCommand(IRCHandler):

    def handle(self, command):
        # If no argument, display agenda event list
        if not command.command_args:
            self.query('list')
            return

        # Check argument user provided is an existing argument
        argument = command.command_args[0]
        if argument not in VALID_ARGUMENTS:
            self.display_unknown_argument()
            return

        # Check if command needs to be voiced
        if argument in VOICED_ARGUMENTS and not command.is_voiced:
            self.display_must_be_voiced()
            return

        # Check all the possible arguments
        if argument == 'help':
            self.display_help()

        elif argument == 'all':
            self.query('list', {'all': True})

        elif argument == 'add':
            regex = re.compile(r'(\d{1,2}\/\d{2}\/\d{4}\s'
                               '\d{1,2}:\d{2})\s"([^"]+)"\s"([^"]+)"(.+)$')
            result = self.test_regex(command, regex)

            if result:
                date, location, title, desc = result.groups()
                self.query('add', {
                    'date': date.strip(),
                    'location': location.strip(),
                    'title': title.strip(),
                    'desc': desc.strip()
                })

        elif argument == 'add_seance':
            regex = re.compile(r'(\d{1,2}\/\d{2}\/\d{4}\s\d{1,2}:\d{2})$')
            result = self.test_regex(command, regex)

            if result:
                date, *_ = result.groups()
                self.query('add_seance', {
                    'date': date.strip()
                })

        elif argument == 'modify':
            regex = re.compile(r'(\d+)\s(titre|lieu|date|status)\s(.+)$')
            result = self.test_regex(command, regex)

            if result:
                id, field, new_value = result.groups()
                self.query('modify', {
                    'id': int(id),
                    'field': field.strip(),
                    'new_value': new_value.strip()
                })

        elif argument == 'remove':
            regex = re.compile(r'(\d+)$')
            result = self.test_regex(command, regex)

            if result:
                id, *_ = result.groups()
                self.query('remove', {
                    'id': int(id),
                })

    def display_must_be_voiced(self):
        self.chanmsg(strings.MUST_BE_VOICED)

    def display_unknown_argument(self):
        self.chanmsg(strings.UNKNOWN_ARGUMENT)
        self.display_help()

    def test_regex(self, command, regex):
        result = regex.match(' '.join(command.command_args[1:]))
        if not result:
            self.display_unknown_argument()
            return None
        return result

    def query(self, command, args=None):
        """Closure for sending a query to the spacestatus microservice."""
        msg = {
            'command': command,
            'source': 'irc'
        }

        # Add args if provided
        if args:
            msg['arguments'] = args

        self.rabbit.publish('agenda.query', msg)

    def display_help(self):
        """Closure for displaying help."""
        for msg in strings.AGENDA_HELP:
            self.chanmsg(msg)


def handle(irc_server, irc_chan, rabbit, command):
    h = AgendaCommand(irc_server, irc_chan, rabbit)
    h.handle(command)

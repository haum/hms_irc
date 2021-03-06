"""Handle agenda events with read and write access."""

import re

from hms_irc import strings
from hms_irc.irc.handlers import SubcommandIRCHandler
from hms_irc.irc.decorators import voiced


class AgendaHandler(SubcommandIRCHandler):
    def query(self, command, args=None):
        """Closure for sending a query to the agenda microservice."""
        msg = {'command': command, 'source': 'irc'}

        if args:
            msg['arguments'] = args

        self.rabbit.publish('agenda.query', msg)

    def display_unknown_argument(self):
        self.chanmsg(strings.UNKNOWN_ARGUMENT)
        self.help()

    def test_regex(self, command, regex):
        result = regex.match(' '.join(command.command_args[1:]))
        if not result:
            self.display_unknown_argument()
            return None
        return result

    def without_subcommand(self):
        self.query('list')

    # Implementation of subcommands

    def cmd_all(self, command):
        self.query('list', {'all': True})

    @voiced
    def cmd_remove(self, command):
        """Supprime un élément.

        !agenda remove id

        """
        regex = re.compile(r'(\d+)$')
        result = self.test_regex(command, regex)

        if result:
            id, *_ = result.groups()
            self.query('remove', {
                'id': int(id),
            })

    @voiced
    def cmd_add(self, command):
        """Ajoute un élément.

        !agenda add JJ/MM/YYYY (h)h:mm "Lieu" "Titre"

        """
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

    @voiced
    def cmd_add_seance(self, command):
        """Ajoute une séance.

        !agenda add_seance JJ/MM/YYYY (h)h:mm

        """
        regex = re.compile(r'(\d{1,2}\/\d{2}\/\d{4}\s\d{1,2}:\d{2})$')
        result = self.test_regex(command, regex)

        if result:
            date, *_ = result.groups()
            self.query('add_seance', {
                'date': date.strip()
            })

    @voiced
    def cmd_modify(self, command):
        """Modifie un élément.

        !agenda modify id [titre|lieu|date|status] nouvelle valeur

        """
        regex = re.compile(r'(\d+)\s(titre|lieu|date|status)\s(.+)$')
        result = self.test_regex(command, regex)

        if result:
            id, field, new_value = result.groups()
            self.query('modify', {
                'id': int(id),
                'field': field.strip(),
                'new_value': new_value.strip()
            })


def get_instance(*args):
    return AgendaHandler(*args)

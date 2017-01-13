import re
#from hms_irc.compat import handle as handle_compat

from hms_irc import strings


#def handle(*args, **kwargs):
#    handle_compat(*args, **kwargs)

VOICED_ARGUMENTS = ['add', 'add_seance', 'remove', 'modify']
VALID_ARGUMENTS = VOICED_ARGUMENTS + ['help', 'all']

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def handle(irc_server, irc_chan, rabbit, command):

    # Define some useful closures

    def query(command, args=None):
        """Closure for sending a query to the spacestatus microservice."""
        msg =  {
            'command': command,
            'source': 'irc'
        }

        # Add args if provided
        if args:
            msg['arguments'] = args

        rabbit.publish('agenda.query', msg)

    def chanmsg(msg):
        """Closure for sending a privmsg on the chan."""
        irc_server.privmsg(irc_chan, msg)

    def help():
        """Closure for displaying help."""
        for msg in strings.AGENDA_HELP:
            chanmsg(msg)

    def testregex(regex):
        result = regex.match(' '.join(command.command_args[1:]))

        if not result:
            chanmsg(strings.UNKNOWN_ARGUMENT)
            help()
            return None

        return result

    if not command.command_args:
        query('list')
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

        if argument == 'all':
            query('list', {'all': True})
        if argument == 'add':
            regex = re.compile(r'(\d{1,2}\/\d{2}\/\d{4}\s\d{1,2}:\d{2})\s"([^"]+)"\s"([^"]+)"(.+)$')
            result = testregex(regex)

            if result:
                date, location, title, desc = result.groups()
                query('add', {
                    'date': date.strip(),
                    'location': location.strip(),
                    'title': title.strip(),
                    'desc': desc.strip()
                })

        elif argument == 'add_seance':
            regex = re.compile(r'(\d{1,2}\/\d{2}\/\d{4}\s\d{1,2}:\d{2})$')
            result = testregex(regex)

            if result:
                date, *_ = result.groups()
                query('add_seance', {
                    'date': date.strip()
                })

        elif argument == 'modify':
            regex = re.compile(r'(\d+)\s(titre|lieu|date|status)\s(.+)$')
            result = testregex(regex)

            if result:
                id, field, new_value = result.groups()
                query('modify', {
                    'id': int(id),
                    'field': field.strip(),
                    'new_value': new_value.strip()
                })

        elif argument == 'remove':
            regex = re.compile(r'(\d+)$')
            result = testregex(regex)

            if result:
                id, *_ = result.groups()
                query('remove', {
                    'id': int(id),
                })
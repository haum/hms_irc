import unittest
from unittest.mock import Mock

from hms_irc.bot import IRCCommand
from hms_irc.transmitters.agenda import handle


def mkcommand(command_args, is_voiced):
    """Builds an IRCCommand for testing purposes."""
    command = IRCCommand(
        nick = "toto",
        is_voiced = is_voiced,
        command_name = "agenda",
        command_args = command_args.split(' '))

    if command.command_args == ['']:
        command.command_args = None

    return command


class AgendaTest(unittest.TestCase):

    """Test that the agenda command parser behaves correctly."""

    def setUp(self):
        self.irc_server = Mock()
        self.irc_server.privmsg = Mock()

        self.irc_chan = "#testhaum"
        self.rabbit = Mock()
        self.rabbit.publish = Mock()

        self.mocked_handle = lambda msg: handle(self.irc_server, self.irc_chan, self.rabbit, msg)

    def test_no_arguments(self):
        """Test to call the agenda command without any argument."""
        command = mkcommand("", False)
        self.mocked_handle(command)
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'list',
            'source': 'irc'})

    def test_help(self):
        """Try to call the help command of agenda."""
        command = mkcommand("help", False)
        self.mocked_handle(command)
        self.rabbit.publish.assert_not_called()

    def test_add(self):
        """Try to add an event to the agenda using the bot."""
        command = mkcommand("add 10/11/2017 17:45 \"Local du HAUM\" \"Test débile\" Un super test complètement débile", True)
        self.mocked_handle(command)
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'add',
            'source': 'irc',
            'arguments': {
                'date': '10/11/2017 17:45',
                'location': 'Local du HAUM',
                'title': 'Test débile',
                'desc': 'Un super test complètement débile'}})

    def test_add_seance(self):
        """Try to add a seance to the agenda using the bot."""
        command = mkcommand("add_seance 10/11/2017 11:42", True)
        self.mocked_handle(command)
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'add_seance',
            'source': 'irc',
            'arguments': {
               'date': '10/11/2017 11:42'}})

    def test_modify(self):
        """Try to modify an event already in the agenda using the bot"""
        command = mkcommand("modify 42 titre Un super nouveau titre", True)
        self.mocked_handle(command)
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'modify',
            'source': 'irc',
            'arguments': {
                'id': 42,
                'field': 'titre',
                'new_value': 'Un super nouveau titre'}})

    def test_remove(self):
        """Try to remove an event already in the agenda using the bot"""
        command = mkcommand("remove 42", True)
        self.mocked_handle(command)
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'remove',
            'source': 'irc',
            'arguments': {
                'id': 42}})
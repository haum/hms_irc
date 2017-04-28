import unittest

from hms_irc.commands.agenda import handle
from hms_irc.commands.tests import CommandBuilder
from hms_irc.mocks import irc_server_mock, rabbit_mock


class AgendaTest(unittest.TestCase):

    """Test that the agenda command parser behaves correctly."""

    def setUp(self):
        self.irc_server = irc_server_mock()
        self.rabbit = rabbit_mock()
        self.irc_chan = "#testhaum"
        self.cb = CommandBuilder()

        self.wrapped_handle = lambda msg: handle(self.irc_server, self.irc_chan,
                                                 self.rabbit, msg)

    # Basic argument checking

    def test_invalid_argument(self):
        """Test to call the agenda command with an invalid argument."""
        self.wrapped_handle(self.cb.args("lolilol").build())
        self.rabbit.publish.assert_not_called()

    def test_bad_argument(self):
        """Test to call a valid command with a bad format."""
        self.wrapped_handle(self.cb.args("remove toto").voiced().build())
        self.rabbit.publish.assert_not_called()

    def test_no_arguments(self):
        """Test to call the agenda command without any argument."""
        self.wrapped_handle(self.cb.build())
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'list',
            'source': 'irc'})

    # Non-voiced commands

    def test_list_all(self):
        """Test list all the events in the agenda."""
        self.wrapped_handle(self.cb.args("all").build())
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'list',
            'arguments': {'all': True},
            'source': 'irc'})

    def test_help(self):
        """Try to call the help command of agenda."""
        self.wrapped_handle(self.cb.args("help").build())
        self.rabbit.publish.assert_not_called()

    # Test that unvoiced user cannot call voiced commands

    def test_command_not_voiced(self):
        """Test to execute a voiced command as non-voiced user."""
        self.wrapped_handle(self.cb.args("remove 42").build())
        self.rabbit.publish.assert_not_called()

    # Voiced commands

    def test_add(self):
        """Try to add an event to the agenda."""
        args = "add 10/11/2017 17:45 \"Local du HAUM\" \"Test débile\" Un " \
              "super test complètement débile"
        self.wrapped_handle(self.cb.args(args).voiced().build())
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'add',
            'source': 'irc',
            'arguments': {
                'date': '10/11/2017 17:45',
                'location': 'Local du HAUM',
                'title': 'Test débile',
                'desc': 'Un super test complètement débile'}})

    def test_add_seance(self):
        """Try to add a seance to the agenda."""
        args = "add_seance 10/11/2017 11:42"
        self.wrapped_handle(self.cb.args(args).voiced().build())
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'add_seance',
            'source': 'irc',
            'arguments': {
               'date': '10/11/2017 11:42'}})

    def test_modify(self):
        """Try to modify an event already in the agenda."""
        args = "modify 42 titre Un super nouveau titre"
        self.wrapped_handle(self.cb.args(args).voiced().build())
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'modify',
            'source': 'irc',
            'arguments': {
                'id': 42,
                'field': 'titre',
                'new_value': 'Un super nouveau titre'}})

    def test_remove(self):
        """Try to remove an event already in the agenda."""
        self.wrapped_handle(self.cb.args("remove 42").voiced().build())
        self.rabbit.publish.assert_called_with('agenda.query', {
            'command': 'remove',
            'source': 'irc',
            'arguments': {
                'id': 42}})
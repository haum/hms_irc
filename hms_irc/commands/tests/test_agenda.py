import pytest

from hms_irc.commands.agenda import get_instance
from hms_irc.commands.tests import build_command, irc_server, irc_chan, rabbit


@pytest.fixture
def instance(irc_server, irc_chan, rabbit):
        return get_instance(irc_server, irc_chan, rabbit)

# Misc

def test_commands_available(instance):
    """Test that all required subcommands are available."""
    required = ["add_seance", "add", "modify", "remove", "all", "help"]
    present = list(instance.subcommand_names())
    for item in required:
        assert("cmd_" + item in present)

# Basic argument checking

def test_invalid_argument(instance):
    """Test to call the agenda command with an invalid argument."""
    instance.handle(build_command("agenda lolilol"))
    instance.rabbit.publish.assert_not_called()

def test_bad_argument(instance):
    """Test to call a valid command with a bad format."""
    instance.handle(build_command("remove toto", voiced=True))
    instance.rabbit.publish.assert_not_called()

def test_no_arguments(instance):
    """Test to call the agenda command without any argument."""
    instance.handle(build_command("agenda"))
    instance.rabbit.publish.assert_called_with('agenda.query', {
        'command': 'list',
        'source': 'irc'})

# Non-voiced commands

def test_list_all(instance):
    """Test list all the events in the agenda."""
    instance.handle(build_command("agenda all"))
    instance.rabbit.publish.assert_called_with('agenda.query', {
        'command': 'list',
        'arguments': {'all': True},
        'source': 'irc'})

def test_help(instance):
    """Try to call the help command of agenda."""
    instance.handle(build_command("agenda help"))
    instance.rabbit.publish.assert_not_called()

# Test that unvoiced user cannot call voiced commands

def test_add_not_voiced(instance):
    """Test to execute a voiced command as non-voiced user."""
    instance.handle(build_command("add 42"))
    instance.rabbit.publish.assert_not_called()

def test_add_seance_not_voiced(instance):
    """Test to execute a voiced command as non-voiced user."""
    instance.handle(build_command("add_seance 42"))
    instance.rabbit.publish.assert_not_called()

def test_modify_not_voiced(instance):
    """Test to execute a voiced command as non-voiced user."""
    instance.handle(build_command("modify 42"))
    instance.rabbit.publish.assert_not_called()

def test_remove_not_voiced(instance):
    """Test to execute a voiced command as non-voiced user."""
    instance.handle(build_command("remove 42"))
    instance.rabbit.publish.assert_not_called()

# Voiced commands

def test_add(instance):
    """Try to add an event to the agenda."""
    args = ("add 10/11/2017 17:45 \"Local du HAUM\" \"Test débile\" Un "
            "super test complètement débile")
    instance.handle(build_command("agenda " + args, voiced=True))
    instance.rabbit.publish.assert_called_with('agenda.query', {
        'command': 'add',
        'source': 'irc',
        'arguments': {
            'date': '10/11/2017 17:45',
            'location': 'Local du HAUM',
            'title': 'Test débile',
            'desc': 'Un super test complètement débile'}})

def test_add_seance(instance):
    """Try to add a seance to the agenda."""
    args = "add_seance 10/11/2017 11:42"
    instance.handle(build_command("agenda " + args, voiced=True))
    instance.rabbit.publish.assert_called_with('agenda.query', {
        'command': 'add_seance',
        'source': 'irc',
        'arguments': {
           'date': '10/11/2017 11:42'}})

def test_modify(instance):
    """Try to modify an event already in the agenda."""
    args = "modify 42 titre Un super nouveau titre"
    instance.handle(build_command("agenda " + args, voiced=True))
    instance.rabbit.publish.assert_called_with('agenda.query', {
        'command': 'modify',
        'source': 'irc',
        'arguments': {
            'id': 42,
            'field': 'titre',
            'new_value': 'Un super nouveau titre'}})

def test_remove(instance):
    """Try to remove an event already in the agenda."""
    args = "remove 42"
    instance.handle(build_command("agenda " + args, voiced=True))
    instance.rabbit.publish.assert_called_with('agenda.query', {
        'command': 'remove',
        'source': 'irc',
        'arguments': {
            'id': 42}})

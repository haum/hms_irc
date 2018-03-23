import pytest

from hms_irc.commands.spacestatus import get_instance
from hms_irc.commands.tests import build_command


@pytest.fixture
def instance(irc_server, irc_chan, rabbit):
        return get_instance(irc_server, irc_chan, rabbit)


# Test the non-voiced commands and behaviors

def test_invalid_argument(instance):
    """Calls the spacestatus command with invalid argument"""
    instance.handle(build_command("spacestatus lol"))
    instance.rabbit.publish.assert_not_called()


def test_check_status(instance):
    """Check that anyone can check the space status."""
    instance.handle(build_command("spacestatus"))
    instance.rabbit.publish.assert_called_with('spacestatus.query', {
        'command': 'status',
        'source': 'irc'
    })


def test_help(instance):
    """Check that the help does not publish a message."""
    instance.handle(build_command("spacestatus help"))
    instance.rabbit.publish.assert_not_called()


# Test the open command with voiced and non-voiced users

def test_open_not_voiced(instance):
    """Test to open the space with non-voiced user."""
    instance.handle(build_command("spacestatus open"))
    instance.rabbit.assert_not_called()


def test_open_voiced(instance):
    """Test to open the space with voiced user."""
    instance.handle(build_command("spacestatus open", voiced=True))
    instance.rabbit.publish.assert_called_with('spacestatus.query', {
        'command': 'open',
        'source': 'irc'
    })

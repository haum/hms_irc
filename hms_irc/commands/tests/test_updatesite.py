import pytest

from hms_irc import settings
from hms_irc.commands.updatesite import get_instance
from hms_irc.commands.tests import build_command


@pytest.fixture
def instance(irc_server, irc_chan, rabbit):
        return get_instance(irc_server, irc_chan, rabbit)


def test_ping(instance):
    command = build_command("updatesite")
    instance.handle(command)
    instance.rabbit.publish.assert_called_with(
        settings.RABBIT_COMMAND_ROUTING_KEY,
        {
            'command': 'updatesite',
            'arg': '',
            'nick': command.nick,
            'is_voiced': False,
        })

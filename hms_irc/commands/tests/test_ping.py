import pytest

from hms_irc import settings
from hms_irc.commands.ping import get_instance
from hms_irc.commands.tests import build_command
from hms_irc.mocks import irc_server_mock, rabbit_mock


@pytest.fixture
def instance():
        irc_server = irc_server_mock()
        rabbit = rabbit_mock()
        irc_chan = "#testhaum"
        instance = get_instance(irc_server, irc_chan, rabbit)
        return instance


def test_ping(instance):
    command = build_command("ping")
    instance.handle(command)
    instance.rabbit.publish.assert_called_with(
        settings.RABBIT_COMMAND_ROUTING_KEY,
        {
            'command': 'ping',
            'arg': '',
            'nick': command.nick,
            'is_voiced': False,
        })

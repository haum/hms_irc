import pytest

from hms_irc.irc.commands import IRCCommand
from hms_irc.mocks import irc_server_mock, rabbit_mock


def build_command(command, nick="toto", voiced=False):
    split_command = command.split(' ')
    return IRCCommand(
        nick=nick,
        is_voiced=voiced,
        command_name=split_command[0],
        command_args=split_command[1:])


@pytest.fixture
def irc_server():
    return irc_server_mock()


@pytest.fixture
def rabbit():
    return rabbit_mock()


@pytest.fixture
def irc_chan():
    return "#testhaum"

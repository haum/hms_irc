import pytest

from hms_irc.commands.toot import get_instance
from hms_irc.commands.tests import build_command, irc_server, irc_chan, rabbit


TEST_MESSAGE = "ceci est un test"

@pytest.fixture
def instance(irc_server, irc_chan, rabbit):
        return get_instance(irc_server, irc_chan, rabbit)


def test_toot_unvoiced(instance):
    instance.handle(build_command("toot " + TEST_MESSAGE))
    instance.rabbit.publish.assert_not_called()


def test_toot_voiced(instance):
    instance.handle(build_command("toot " + TEST_MESSAGE, voiced=True))
    instance.rabbit.publish.assert_called_once_with('mastodon.toot', {
        'message': TEST_MESSAGE, 'source': 'irc'})


def test_toot_no_message(instance):
    instance.handle(build_command("toot"))
    instance.rabbit.publish.assert_not_called()

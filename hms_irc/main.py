import logging
from threading import Thread
import time

import coloredlogs

from hms_irc.bot import MyBot
from hms_irc.mesg import Rabbit
from hms_irc import settings


def get_logger():
    return logging.getLogger(__name__)


def main():

    # Logging
    logging.basicConfig(
        format='%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s',
        level=logging.INFO)

    coloredlogs.install(level='INFO')

    # Connect to Rabbit
    rabbit = Rabbit()
    rabbit.connect(settings.RABBIT_HOST)

    # IRC bot settings
    bot = MyBot(settings.IRC_CHAN, settings.IRC_NAME, settings.IRC_SERVER)

    # Add callback
    rabbit.listenners.append(bot.rabbit)

    # Start IRC thread
    irc_thread = Thread(target=bot.start)
    irc_thread.start()

    # Wait for IRC bot to connect before fetching
    # TODO: use passive wait using a callback instead
    while not bot.joined:
        get_logger().warning('Waiting for IRC bot to join channel')
        time.sleep(1)

    # Start the rabbit receive thread
    rabbit_thread = Thread(target=rabbit.consume)
    rabbit_thread.start()

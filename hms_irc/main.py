import sys
import logging
from threading import Thread

import coloredlogs

from hms_base.client import Client

from hms_irc.bot import MyBot
from hms_irc import settings


def get_logger():
    return logging.getLogger(__name__)


def main():
    """Entry point of the program."""

    # Logging
    coloredlogs.install(level='INFO')

    # Connect to Rabbit
    rabbit = Client('hms_irc', settings.RABBIT_EXCHANGE,
                    settings.RABBIT_ROUTING_KEYS)

    rabbit.connect(settings.RABBIT_HOST)

    rabbit_thread = Thread(target=rabbit.start_consuming)
    rabbit_thread.setDaemon(True)  # To kill the thread when main is gone

    # IRC bot settings
    bot = MyBot(settings.IRC_CHAN, settings.IRC_NAME, settings.IRC_SERVER)
    bot.rabbit = rabbit

    # Add callbacks
    rabbit.listeners.append(bot.handle_rabbit_msg)

    def chan_joined():
        """Callback that will start the RabbitMQ receive thread."""
        if not rabbit_thread.is_alive():
            get_logger().info('Starting RabbitMQ consume thread...')
            rabbit_thread.start()
        else:
            get_logger().warning("Chan joined but RabbitMQ thread is alive")

    bot.join_callback = chan_joined

    # Start IRC thread that will start Rabbit thread using callback
    try:
        get_logger().info('Starting IRC bot...')
        bot.start()
    except KeyboardInterrupt:
        get_logger().critical("Got a KeyboardInterrupt")
        get_logger().info("Disconnecting from Rabbit")

        # Beautiful RabbiMQ shutdown attempt
        rabbit.stop_consuming()
        rabbit.disconnect()

        # Beautiful IRC shutdown
        get_logger().info("Disconnecting from IRC")
        bot.die(msg="got a KeyboardInterrupt in my face! >_<")

        # Exit and kill daemon thread
        sys.exit(0)

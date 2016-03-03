import logging
from threading import Thread

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

    rabbit_thread = Thread(target=rabbit.consume)
    rabbit_thread.setDaemon(True)  # To kill the thread when main is gone

    # IRC bot settings
    bot = MyBot(settings.IRC_CHAN, settings.IRC_NAME, settings.IRC_SERVER)

    # Add callbacks
    rabbit.listenners.append(bot.handle_rabbit_msg)

    def chan_joined():
        # Start the rabbit receive thread
        get_logger().info('Starting RabbitMQ consume thread...')
        rabbit_thread.start()

    bot.join_callback = chan_joined

    # Start IRC thread that will start Rabbit thread using callback
    try:
        get_logger().info('Starting IRC bot...')
        bot.start()
    except KeyboardInterrupt:
        get_logger().critical("Got a KeyboardInterrupt")
        get_logger().info("Disconnecting from Rabbit")

        rabbit.stop_consume()
        rabbit.disconnect()

        get_logger().info("Disconnecting from IRC")
        bot.die(msg="got a KeyboardInterrupt in my face!")


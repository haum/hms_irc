import logging
from threading import Thread
import time

import coloredlogs

from bot import MyBot
from mesg import Rabbit

def get_logger():
    return logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s',
    level=logging.INFO)


coloredlogs.install(level='INFO')

rabbit = Rabbit()

rabbit.connect('10.1.0.1')

bot = MyBot("#testhaum", "rabbitmq", "irc.freenode.net")
rabbit.listenners.append(bot.rabbit)

irc_thread = Thread(target=bot.start)
irc_thread.start()

while not bot.joined:
    get_logger().warning('Waiting for IRC bot to join channel')
    time.sleep(1)

rabbit_thread = Thread(target=rabbit.consume)
rabbit_thread.start()

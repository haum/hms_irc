# Configuration file for hms_irc

# RabbitMQ

RABBIT_HOST = '10.1.0.1'          # Address of the server
RABBIT_EXCHANGE = 'haum'          # Name of the direct echanger
RABBIT_ROUTING_KEYS = ['reddit']  # List of routing keys to listen to

# IRC

IRC_SERVER = 'irc.freenode.net'  # Server to join
IRC_CHAN = '#testhaum'           # Chan to join (do not forget the #)
IRC_NAME = 'rabbitmq'            # Name of the bot on the server

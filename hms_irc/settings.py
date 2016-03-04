# Configuration file for hms_irc

# RabbitMQ

RABBIT_HOST = 'localhost'         # Address of the server
RABBIT_EXCHANGE = 'haum'          # Name of the direct echanger
RABBIT_ROUTING_KEYS = ['reddit']  # List of routing keys to listen to

# IRC

IRC_SERVER = 'irc.freenode.net'  # Server to join
IRC_CHAN = '#testhaum'           # Chan to join (do not forget the #)
IRC_NAME = 'hms_irc'             # Name of the bot on the server

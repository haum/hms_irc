# Configuration file for hms_irc

# RabbitMQ

RABBIT_HOST = 'localhost'                   # Address of the server
RABBIT_EXCHANGE = 'haum'                    # Name of the direct exchanger
RABBIT_COMMAND_ROUTING_KEY = 'irc_command'  # Routing key for irc command

PING_NAME = 'hms_irc'

# List of routing keys to listen to
RABBIT_ROUTING_KEYS = ['reddit', 'irc_debug', 'ping', 'spacestatus.*']

# IRC

IRC_SERVER = 'irc.freenode.net'  # Server to join
IRC_CHAN = '#testhaum'           # Chan to join (do not forget the #)
IRC_NAME = 'hms_irc'             # Name of the bot on the server

# Import prod settings if existing

try:
    from hms_irc.settings_prod import *
except ImportError:
    pass
import sys
import json
import logging

import coloredlogs

from hms_base.client import Client


def get_logger():
    return logging.getLogger(__name__)


def usage():
    print("usage: debug.py <your message>")


def main():
    coloredlogs.install(level='INFO')

    # Check we have some args
    if len(sys.argv) <= 1:
        usage()
        sys.exit(1)

    message = ' '.join(sys.argv[1:])

    c = Client('hms_irc_debug', 'haum', [])
    c.connect()

    post = {
        'privmsg': message
    }

    message = json.dumps(post)

    get_logger().info("Publising message...")

    c.publish('irc_debug', post)

    get_logger().info("Sent message '{}'".format(message))

    get_logger().info("Closing connection")
    c.disconnect()


if __name__ == "__main__":
    main()

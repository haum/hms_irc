import sys
import json
import logging

import pika
import coloredlogs


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

    get_logger().info("Connecting to RabbitMQ server...")
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    get_logger().info("Creating channel...")
    channel = conn.channel()

    get_logger().info("Declarating exchanger")
    channel.exchange_declare(exchange='haum', type='direct')

    post = {
        'privmsg': message
    }

    message = json.dumps(post)

    get_logger().info("Publising message...")

    channel.basic_publish(
        exchange='haum',
        routing_key='irc_debug',
        body=message)

    get_logger().info("Sent message \"{}\"".format(message))

    get_logger().info("Closing connection")
    conn.close()

if __name__ == "__main__":
    main()

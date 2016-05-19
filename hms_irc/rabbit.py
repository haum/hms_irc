import logging
import json

import pika

from hms_irc import settings


def get_logger():
    return logging.getLogger(__name__)


class RabbitClient:

    def __init__(self):
        self.listeners = []
        self.exchange = settings.RABBIT_EXCHANGE
        self.routing_keys = settings.RABBIT_ROUTING_KEYS
        self.command_routing_key = settings.RABBIT_COMMAND_ROUTING_KEY

    def connect(self, host):
        """Connect to a RabbitMQ server and set up receive callback."""

        # Connect

        get_logger().info("Connecting to RabbitMQ server...")

        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.conn.channel()

        # Exchanger

        get_logger().info("Declaring direct exchanger {}...".format(
            self.exchange))

        self.channel.exchange_declare(exchange=self.exchange, type='direct')

        # Create queue

        get_logger().info("Creating RabbitMQ queue...")
        result = self.channel.queue_declare(exclusive=True)

        self.queue_name = result.method.queue

        # Binding

        for routing_key in self.routing_keys:
            get_logger().info(
                "Binding queue to exchanger {} with routing key {}...".format(
                    self.exchange, routing_key))

            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key=routing_key)

        # Callback

        get_logger().info("Binding callback...")
        self.channel.basic_consume(
            self._callback, queue=self.queue_name, no_ack=True)

    def publish_command(self, data):
        """Send a command with internal routing key to the exchange."""
        get_logger().info("Publishing command {}.".format(data))

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.command_routing_key,
            body=json.dumps(data)
        )

    def consume(self):
        """Start the infinite blocking consume process."""
        get_logger().info("Starting passive consuming...")
        self.channel.start_consuming()

    def stop_consume(self):
        """Stop the consume process."""
        get_logger().info("Stopping passive consuming...")
        self.channel.stop_consuming()

    def _callback(self, *args):
        """Internal method that will be called when receiving message."""

        get_logger().info("Message received! Calling listeners...")

        for li in self.listeners:
            li(*args)

    def disconnect(self):
        """Disconnect from the RabbitMQ server."""
        get_logger().info("Disconnecting from RabbitMQ server...")
        self.conn.close()

import logging

import pika


def get_logger():
    return logging.getLogger(__name__)


class Rabbit:

    def __init__(self):
        self.listenners = []

    def connect(self, host):
        get_logger().info("Connecting to RabbitMQ server...")

        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.conn.channel()

        get_logger().info("Declaring exhanger...")
        self.channel.exchange_declare(exchange='haum', type='fanout')

        get_logger().info("Creating RabbitMQ queue...")
        result = self.channel.queue_declare(exclusive=True)

        self.queue_name = result.method.queue

        get_logger().info("Binding queue to exchanger...")
        self.channel.queue_bind(exchange='haum', queue=self.queue_name)

        get_logger().info("Binding callback...")
        self.channel.basic_consume(
            self.callback, queue=self.queue_name, no_ack=True)

    def consume(self):
        get_logger().info("Starting passive consuming...")
        self.channel.start_consuming()

    def callback(self, *args):
        get_logger().info("Callback called")
        for li in self.listenners:
            li(*args)

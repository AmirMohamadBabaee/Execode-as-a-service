import pika

AMQP_URL = "amqps://grawkbwj:nbMRsg9sF8lNGnrKjGM24BQLC7tSaUQS@hummingbird.rmq.cloudamqp.com/grawkbwj" 

class RabbitMQHandler():

    def __init__(self):
        self.queue_name = "run"
        self.connection, self.channel = self.connect()
        self.declare_queue(self.queue_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def connect(self):
        connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        channel = connection.channel()
        return connection, channel

    def declare_queue(self, queue_name:str):
        if self.channel:
            self.channel.queue_declare(queue=queue_name)

    def publish_on_queue(self, content):
        if self.channel:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=f"{content}")

    def consume_on_queue(self, callback):
        if self.channel:
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

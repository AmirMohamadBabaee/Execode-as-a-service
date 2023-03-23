import pika


class RabbitMQHandler():

    AMQP_URL = "amqps://grawkbwj:nbMRsg9sF8lNGnrKjGM24BQLC7tSaUQS@hummingbird.rmq.cloudamqp.com/grawkbwj" 

    def __init__(self):
        self.connection, self.channel = self.connect()

    def __enter__(self):
        return self.channel

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def connect(self):
        connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        channel = connection.channel()
        return connection, channel

    def declare_queue(self, queue_name:str):
        if self.channel:
            self.channel.queue_declare(queue=queue_name)

    def publish_on_queue(self, queue_name:str, content):
        if self.channel:
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=content)

    def consume_on_queue(self, queue_name:str, callback):
        if self.channel:
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

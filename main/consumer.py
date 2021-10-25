import pika

params = pika.URLParameters("amqps://vfchomdw:1a3bInD6To-Z7MOlDXamu0u8cbY3hYkR@hornet.rmq.cloudamqp.com/vfchomdw")

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="main")


def callback(channel, method, properties, body):
    print("Received in main")
    print(body)


channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=False)

print("Launched")

channel.start_consuming()
channel.close()

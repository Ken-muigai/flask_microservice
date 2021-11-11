# amqps://vfchomdw:1a3bInD6To-Z7MOlDXamu0u8cbY3hYkR@hornet.rmq.cloudamqp.com/vfchomdw
import pika, json

params = pika.URLParameters("amqps://vfchomdw:1a3bInD6To-Z7MOlDXamu0u8cbY3hYkR@hornet.rmq.cloudamqp.com/vfchomdw")

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties =pika.BasicProperties(method)
    channel.basic_publish(exchange="", routing_key="admin", body=json.dumps(body), properties=properties)

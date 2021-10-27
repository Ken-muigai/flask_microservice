import json
import pika

from main import Product, db

params = pika.URLParameters("amqps://vfchomdw:1a3bInD6To-Z7MOlDXamu0u8cbY3hYkR@hornet.rmq.cloudamqp.com/vfchomdw")

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="main")


def callback(ch, method, properties, body):
    print("Launched")
    print("Received in main")
    data = json.loads(body)
    print(data)

    if properties.content_type == "Product Added":
        product = Product(id=data["id"], title=data["name"], image=data["image"])
        db.session.add(product)
        db.session.commit()
    elif properties.content_type == "Product Updated":
        product = Product.query.get(id=data["id"])
        product.title = data["name"]
        product.image = data["image"]
        db.session.commit()
    elif properties.content_type == "Product Destroyed":
        product = Product.query.get(id=data["id"])
        db.session.delete(product)
        db.session.commit()



channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=False)
channel.start_consuming()
channel.close()


import json
import pika

from main import Product, db

params = pika.URLParameters("amqps://vfchomdw:1a3bInD6To-Z7MOlDXamu0u8cbY3hYkR@hornet.rmq.cloudamqp.com/vfchomdw")

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="main", durable=False, auto_delete=False)


def callback(ch, method, properties, body):
    print("Launched")
    print("Received in main")
    data = json.loads(body)
    print(data)

    if properties.content_type == "Product Added":
        product = Product(id=data["id"], title=data["title"], image=data["image"], likes=data["likes"])
        db.session.add(product)
        db.session.commit()
    elif properties.content_type == "Product Updated":
        product = Product.query.get(data["id"])
        product.title = data["title"]
        product.image = data["image"]
        db.session.commit()
        print("product updated")
    elif properties.content_type == "Product Destroyed":
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()



channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()

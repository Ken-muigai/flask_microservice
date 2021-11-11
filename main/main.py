from dataclasses import dataclass

from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
import requests

from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:myuser@db/myuser"
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    likes: int
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    likes = db.Column(db.Integer, nullable=False)


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    # UniqueConstraint("user_id", 'product_id', name='user_product_unique')


@app.route("/api/products")
def index():
    return jsonify(Product.query.all())


@app.route("/api/products/<int:id>/like", methods=["POST"])
def like(id):
    req = requests.get("http://172.17.0.1:8000/api/user")
    json = req.json()

    try:
        print(json["id"], id)
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish('Product Liked', id)
    except:
        abort(400, "did not work")


    return jsonify({
        "Message": "Liked"
    })


@app.route("/api/delete/", methods=["DELETE"])
def destroyer():
    db.session.query(Product).delete()
    db.session.commit()
    return "Deleted"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

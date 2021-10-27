from dataclasses import dataclass

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
import requests
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:myuser@db/myuser"
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    produc_id = db.Column(db.Integer)
    UniqueConstraint("user_id", 'product_id', name='user_product_unique')


@app.route("/api/products")
def index():
    return jsonify(Product.query.all())



@app.route("/api/products/<int:id>/like", methods=["POST"])
def like(id):
    req = requests.get("http://docker.for.linux.localhost:8000/api/user")
    return jsonify(req)












# @app.route("/api/delete/")
# def destroyer():
#     products = Product.query.delete()
#     db.session.delete(products)
#     db.session.commit()
#     return "Deleted"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

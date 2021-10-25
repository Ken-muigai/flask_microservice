from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:myuser@db/myuser"
CORS(app)

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)



class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    produc_id = db.Column(db.Integer)
    UniqueConstraint("user_id", 'product_id', name='user_product_unique')


@app.route("/")
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

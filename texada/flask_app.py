from flask import Flask
from flask import request
from flask import jsonify
from db import session_scope
from models import Product

texada_api = Flask("texada_api")

@texada_api.route("/")
def root():
	return "<h1>Welcome to Xintong's project!/</h1>"


@texada_api.route("/products/<pid>", methods=["GET"])
def get_product(pid):
	with session_scope() as session:
		product = session.query(
			Product
		).filter(
			Product.id == pid
		).one_or_none()

		response = {
					"description": product.description,
					"id": product.id,
					"datetime": product.datetime,
					"longitude": product.longitude,
					"latitude": product.latitude,
					"elevation": product.elevation,}
	return jsonify(response)


if __name__ == '__main__':
    texada_api.run()

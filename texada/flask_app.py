from flask import Flask
from flask import request
from flask import jsonify
from db import session_scope
from models import Product
from errors import ClientError

texada_api = Flask("texada_api")

@texada_api.errorhandler(ClientError)
def handle_client_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


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
		
		if not product:
			raise ClientError("Oops! Product not found. Please enter a different id.")		

		response = {"description": product.description,
					"id": product.id,
		#			"datetime": product.datetime,
		#			"longitude": product.longitude,
		#			"latitude": product.latitude,
		#			"elevation": product.elevation,
                    }
	return jsonify(response)




if __name__ == '__main__':
    texada_api.run()

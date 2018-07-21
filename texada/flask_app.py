from flask import Flask
from flask import request
from flask import jsonify
from db import session_scope
from models import Product
from models import LocationRecord as Record
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


@texada_api.route("/products/<int:pid>", methods=["GET"])
def get_product(pid):
    with session_scope() as session:
        product = session.query(
            Product
        ).filter(
            Product.id == pid
        ).one_or_none()
        
        if not product:
            raise ClientError("Oops! Product not found")
    
        records = session.query(
            Record
        ).filter(
            Record.product_id == pid
        ).all()
		
        response = {"description": product.description,
                    "records":[{
                        "id": record.id,
                        "datetime": record.datetime,
                        "longitude": record.longitude,
                        "latitude": record.latitude,
                        "elevation": record.elevation,
                    } for record in records]}
	return jsonify(response)


@texada_api.route("/location_records", methods=["POST"])
def add_recrod():
    keys = ["description","datetime","longitude","latitude","elevation"]
    args = request.get_json()
    print "******DEBUG*******:",args
    for k in keys:
        if k not in args:
            err = "missing argument {}".format(k)
            raise ClientError(err)     
    with session_scope() as session:
        product = session.query(
            Product
        ).filter(
            Product.description == args["description"]
        ).one_or_none()
        if not product:
            p = Product(description = args["description"])
            session.add(p)
            session.flush()
            pid = p.id
        else:
            pid = product.id

        record = Record(
                    product_id = pid,
                    datetime = args["datetime"],
                    longitude = args["longitude"],
                    latitude = args["latitude"],
                    elevation = args["elevation"],    
        )
        session.add(record)
        session.flush()
        response = {"record_id": record.id}
    return jsonify(response)


@texada_api.route("/location_records/<int:record_id>", methods=["DELETE","PUT"])
def modify_record(record_id):
    args = request.get_json()
    with session_scope() as session:
        record = session.query(
            Record
        ).filter(
            Record.id == record_id
        ).one_or_none()
        if not record:  
            raise ClientError("Oops! Record not found")
        if request.method == "DELETE":
            session.delete(record)
            session.flush()
            response = "successfully deleted record {}".format(record_id)
        if request.method == "PUT":
            record.longitude = args.get("longitude", record.longitude)
            record.latitude = args.get("latitude",record.latitude)
            record.elevation = args.get("elevation", record.elevation)
            response = "successfully updated record {}".format(record_id)
    return response


if __name__ == '__main__':
    texada_api.run()

from flask import Flask
from flask import request
from flask import jsonify
from db import session_scope
from models import Product
from models import LocationRecord as Record
from errors import ClientError
# input validation
from webargs import fields
from webargs.flaskparser import parser
from webargs.flaskparser import use_args

import datetime

PAGE_START = 1
PAGE_LIMIT = 10

texada_api = Flask('texada_api')

@parser.error_handler
def handle_args_error(err, request, con):
    raise ClientError(err.message)


@texada_api.errorhandler(ClientError)
def handle_client_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@texada_api.route('/')
def root():
	return "<h1>Welcome to Xintong's project!/</h1>"


@texada_api.route('/products', methods=['GET'])
@use_args({})
def get_all_products(args):
    with session_scope() as session:
        products = session.query(
            Product
        ).all()
        response = {'products': [{'description': product.description, 
                                  'product_id': product.id}
                                for product in products]
        }
        return jsonify(response)
       

#implement pagination for product 
@texada_api.route('/products/page', methods=['GET'])
@use_args({
    'start': fields.Int(missing = PAGE_START),
    'limit':fields.Int(missing = PAGE_LIMIT)
})
def get_products_paged(args):
    print args
    return jsonify(get_paginated_list(
        Product, 
        '/products/page', 
        args['start'],
        args['limit']
    ))

def get_paginated_list(klass, url, start, limit):
    # check if page exists
    with session_scope() as session:
        results = session.query(klass).all()
        count = len(results)
        if (count < start):
            raise ClientError('Page not found')
        # make response
        obj = {}
        obj['start'] = start
        obj['limit'] = limit
        obj['count'] = count
        # make URLs
        # make previous url
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        # make next url
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        # finally extract result according to bounds
        res_this_page = results[(start - 1):(start - 1 + limit)]
        obj['results'] =[{
            'id': product.id,
            'description': product.description,
        } for product in res_this_page]
        return obj



@texada_api.route('/products/<int:pid>', methods=['GET'])
def get_product_by_id(pid):
    with session_scope() as session:
        product = session.query(
            Product
        ).filter(
            Product.id == pid
        ).one_or_none()
        
        if not product:
            raise ClientError('Oops! Product not found')
    
        records = session.query(
            Record
        ).filter(
            Record.product_id == pid
        ).all()
		
        response = {'product_id': pid,
                    'description': product.description,
                    'records':[{
                        'record_id': record.id,
                        'datetime': record.datetime,
                        'longitude': record.longitude,
                        'latitude': record.latitude,
                        'elevation': record.elevation,
                    } for record in records]}
	return jsonify(response)


@texada_api.route('/location_records', methods=['POST'])
@use_args({
    'longitude': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'description': fields.Str(required=True),
    'datetime': fields.Str(required=True),
    'elevation': fields.Float(required=True),
})
def add_recrod(args):
    dt = args['datetime']
    try:
        start = dt[:19]
        end = dt[19:]
        datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        datetime.datetime.strptime(end, '-%H:%M')
    except ValueError:
        raise ClientError('Invalid datetime format, should be yyyy-mm-ddTHH:MM:SS-HH:MM')

    with session_scope() as session:
        product = session.query(
            Product
        ).filter(
            Product.description == args['description']
        ).one_or_none()
        if not product:
            p = Product(description = args['description'])
            session.add(p)
            session.flush()
            pid = p.id
        else:
            pid = product.id

        record = Record(
                    product_id = pid,
                    datetime = args['datetime'],
                    longitude = args['longitude'],
                    latitude = args['latitude'],
                    elevation = args['elevation'],    
        )
        session.add(record)
        session.flush()
        response = {'record_id': record.id}
    return jsonify(response)


@texada_api.route('/location_records/<int:record_id>', methods=['DELETE','PUT'])
@use_args({
    'longitude': fields.Float(),
    'latitude': fields.Float(),
    'elevation': fields.Float(),
    'datetime': fields.Str(),
})

def modify_record(args, record_id):
    with session_scope() as session:
        record = session.query(
            Record
        ).filter(
            Record.id == record_id
        ).one_or_none()
        if not record:  
            raise ClientError('Oops! Record not found')
        if request.method == 'DELETE':
            session.delete(record)
            response = 'successfully deleted record {}'.format(record_id)
        if request.method == 'PUT':
            #validate datime
            if args.get('datetime', None):
                dt = args['datetime']
                try:
                    start = dt[:19]
                    end = dt[19:]
                    datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
                    datetime.datetime.strptime(end, '-%H:%M')
                except ValueError:
                    raise ClientError('Invalid datetime format, should be yyyy-mm-ddTHH:MM:SS-HH:MM')
                record.datetime = dt
            record.longitude = args.get('longitude', record.longitude)
            record.latitude = args.get('latitude',record.latitude)
            record.elevation = args.get('elevation', record.elevation)
            response = 'successfully updated record {}'.format(record_id)
    return response


if __name__ == '__main__':
    texada_api.run()

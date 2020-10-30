'''Main app file'''

import logging as log

from flask import Flask, request, json, Response
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)


class MongoAPI:

    def __init__(self):
        log.basicConfig(handlers=[log.FileHandler(filename="log_app.txt", encoding='utf-8', mode='a+')], level=log.DEBUG, format='%(asctime)s - %(message)s')

        client = MongoClient("mongodb://localhost:27017/")
        database = client['store_db']

        self.collection = database['orders']

    def find_orders(self, order_id_list):
        '''Find orders with specified IDs'''
        log.info('Find orders data: {}'.format(str(order_id_list)))

        response = self.collection.find({"Order_ID": {"$in": order_id_list}})
        serialised_response = dumps(response)

        status = {'Status': 'Successfully finded {} order(s)'.format(len(serialised_response))
                   if  len(serialised_response) > 0 else "Nothing was found."}
        log.info(str(status))
        return serialised_response

    def write_order(self, new_order_data):
        '''Write new order to DB'''
        log.info('Writing order: {}'.format(new_order_data["Order_ID"]))

        if self.collection.find_one({"Order_ID":new_order_data["Order_ID"]}) is not None:
            status = {'Status': 'Order allredy exist '}
        else:
            response = self.collection.insert_one(new_order_data)
            status = {'Status': 'Order Successfully writed', 'Order_ID': str(new_order_data["Order_ID"])
                      if response.inserted_id is not None else "Nothing was writed."}
        log.info(str(status))
        return status

    def update_order(self, updated_order_data):
        '''Update existing order in DB'''
        log.info('Updating order: {}'.format(updated_order_data["Order_ID"]))

        data_to_update = self.collection.find_one({"Order_ID": updated_order_data["Order_ID"]})
        updated_data = {"$set": updated_order_data}

        response = self.collection.update_one(data_to_update, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}

        log.info(str(output))
        return output

    def delete_order(self, order_to_delete_id):
        '''Delete existing order from DB'''
        log.info('Deleting order: {}'.format(order_to_delete_id["Order_ID"]))

        response = self.collection.delete_one(order_to_delete_id)

        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}

        log.info(str(output))
        return output

@app.route('/')
def base():
    '''Main page response'''
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/ordersdb', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {} or 'Order_ID' not in data:
        return Response(response=json.dumps({"Error": "Please provide order information"}),
                        status=400,
                        mimetype='application/json')
    api = MongoAPI()
    response = api.write_order(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/ordersdb', methods=['GET'])
def mongo_read():
    data = request.json
    if data is None or data == {} or 'Order_ID' not in data:
        return Response(response=json.dumps({"Error": "Please provide JSON with orders ID"}),
                        status=400,
                        mimetype='application/json')
    list_of_orders_id = data["Order_ID"]
    api = MongoAPI()
    response = api.find_orders(list_of_orders_id)

    return Response(response=response,
                    status=200,
                    mimetype='application/json')

@app.route('/ordersdb', methods=['PUT'])
def mongo_update():
    data = request.json
    if data is None or data == {} or 'Order_ID' not in data:
        return Response(response=json.dumps({"Error": "Please provide order information"}),
                        status=400,
                        mimetype='application/json')
    api = MongoAPI()
    response = api.update_order(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/ordersdb', methods=['DELETE'])
def mongo_delete():
    data = request.json
    if data is None or data == {} or 'Order_ID' not in data:
        return Response(response=json.dumps({"Error": "Please provide order information"}),
                        status=400,
                        mimetype='application/json')
    api = MongoAPI()
    response = api.delete_order(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
                    
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='localhost')

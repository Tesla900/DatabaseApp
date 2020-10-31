'''Main app file'''
from flask import Flask, request, json, Response
from mongoapi import MongoAPI

app = Flask(__name__)

@app.route('/')
def base():
    '''Main page response'''
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/ordersdb', methods=['POST'])
def mongo_write():
    '''POST request handler'''
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
    '''GET request handler'''
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
    '''PUT request handler'''
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
    '''DELETE request handler'''
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

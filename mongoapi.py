'''MongoDB API'''

import logging as log
from pymongo import MongoClient
from bson.json_util import dumps

class MongoAPI:
    '''Main DB API'''
    def __init__(self):
        log.basicConfig(handlers=[log.FileHandler(filename="log_app.txt", encoding='utf-8', mode='a+')], level=log.DEBUG, format='%(asctime)s - %(message)s')

        #For local tests only
        client = MongoClient("mongodb://localhost:27017/")

        #For docker-compose based deploy
        #client = MongoClient("mongodb://datastore:27017/")

        database = client['store_db']

        self.collection = database['orders']

    def find_orders(self, order_id_list):
        '''Find orders with specified IDs'''
        log.info('Find orders data: {}'.format(str(order_id_list)))

        response = self.collection.find({"Order_ID": {"$in": order_id_list}})
        serialised_response = dumps(response)

        output = {'Status': 'Successfully finded {} order(s)'.format(response.count())
                   if  response.count() > 0 else "Nothing was found"}
        log.info(str(output))
        return serialised_response

    def write_order(self, new_order_data):
        '''Write new order to DB'''
        log.info('Writing order: {}'.format(new_order_data["Order_ID"]))

        if self.collection.find_one({"Order_ID":new_order_data["Order_ID"]}) is not None:
            output = {'Status': 'Order allredy exist'}
        else:
            response = self.collection.insert_one(new_order_data)
            output = {'Status': 'Order successfully writed'
                      if response.inserted_id is not None else "Nothing was writed"}
        log.info(str(output))
        return output

    def update_order(self, updated_order_data):
        '''Update existing order in DB'''
        log.info('Updating order: {}'.format(updated_order_data["Order_ID"]))

        data_to_update = self.collection.find_one({"Order_ID": updated_order_data["Order_ID"]})
        if data_to_update is not None:
            updated_data = {"$set": updated_order_data}
            response = self.collection.update_one(data_to_update, updated_data)
            output = {'Status': 'Order successfully updated'
                      if response.modified_count > 0 else "Nothing was updated"}
        else:
            output = {'Status': 'Order not found'}

        log.info(str(output))
        return output

    def delete_order(self, order_to_delete_id):
        '''Delete existing order from DB'''
        log.info('Deleting order: {}'.format(order_to_delete_id["Order_ID"]))

        response = self.collection.delete_one(order_to_delete_id)

        output = {'Status': 'Order successfully deleted'
                  if response.deleted_count > 0 else "Order not found"}

        log.info(str(output))
        return output

    def clear_db(self):
        deleted = self.collection.delete_many({})

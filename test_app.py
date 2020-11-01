'''Basic API tests'''
import unittest
import json

from app import app
from mongoapi import MongoAPI

class FlaskTestCase(unittest.TestCase):
    '''Basic API tests class'''

    def setUp(self):
        '''Test setup'''
        self.app = app.test_client()
        self.api = MongoAPI("localhost")
        self.api.clear_db()

    def test_index(self):
        '''Ensure that Flask was set up correctly'''
        response = self.app.get('/', content_type='application/json')
        self.assertEqual('UP', response.json['Status'])

    def test_database_add(self):
        '''Ensure POST method DB add order is working'''
        # Given
        payload = json.dumps({
            "Order_ID": 1,
            "Order_list": ["apple", "banana", "orange"],
            "Total_price": 570.24,
            "Phone": "+380501234567",
            "Email": "example1@test.com"
        })
        possible_response1 = "Order successfully writed"
        possible_response2 = "Order allredy exist"

        # When
        response = self.app.post('/ordersdb', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(possible_response1, response.json['Status'])
        self.assertEqual(response.status_code, 200)

        # When
        response = self.app.post('/ordersdb', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(possible_response2, response.json['Status'])
        self.assertEqual(response.status_code, 200)
        self.api.clear_db()

    def test_database_update(self):
        '''Ensure PUT method DB update order is working'''
        # Given
        payload1 = json.dumps({
            "Order_ID": 1,
            "Order_list": ["apple", "banana", "orange"],
            "Total_price": 570.24,
            "Phone": "+380501234567",
            "Email": "example1@test.com"
        })
        payload2 = json.dumps({
            "Order_ID": 1,
            "Order_list": ["apple", "banana", "pineapple"],
            "Total_price": 657.24,
            "Phone": "+380501234567",
            "Email": "example1@test.com"
        })
        possible_response1 = "Order successfully updated"
        possible_response2 = "Nothing was updated"

        # When
        self.app.post('/ordersdb', headers={"Content-Type": "application/json"}, data=payload1)
        response = self.app.put('/ordersdb', headers={"Content-Type": "application/json"}, data=payload2)

        # Then
        self.assertEqual(possible_response1, response.json['Status'])
        self.assertEqual(response.status_code, 200)

        # When
        response = self.app.put('/ordersdb', headers={"Content-Type": "application/json"}, data=payload2)

        # Then
        self.assertEqual(possible_response2, response.json['Status'])
        self.assertEqual(response.status_code, 200)
        self.api.clear_db()

    def test_database_get(self):
        '''Ensure GET method DB find order is working'''
        # Given
        payload1 = json.dumps({
            "Order_ID": 1,
            "Order_list": ["apple", "banana", "orange"],
            "Total_price": 570.24,
            "Phone": "+380501234567",
            "Email": "example1@test.com"
        })
        payload2 = json.dumps({
            "Order_ID": 2,
            "Order_list": ["apple", "banana", "pineapple"],
            "Total_price": 657.24,
            "Phone": "+380576543210",
            "Email": "example@test.com"
        })
        payload3 = json.dumps({
            "Order_ID": [1, 2]
        })

        possible_response1 = 1
        possible_response2 = 2

        # When
        self.app.post('/ordersdb', headers={"Content-Type": "application/json"}, data=payload1)
        self.app.post('/ordersdb', headers={"Content-Type": "application/json"}, data=payload2)
        response = self.app.get('/ordersdb', headers={"Content-Type": "application/json"}, data=payload3)

        # Then
        self.assertEqual(possible_response1, response.json[0]['Order_ID'])
        self.assertEqual(possible_response2, response.json[1]['Order_ID'])
        self.assertEqual(response.status_code, 200)
        self.api.clear_db()

    def test_database_delete(self):
        '''Ensure DELETE method DB delete order is working'''
        # Given
        payload1 = json.dumps({
            "Order_ID": 1,
            "Order_list": ["apple", "banana", "orange"],
            "Total_price": 570.24,
            "Phone": "+380501234567",
            "Email": "example1@test.com"
        })

        payload2 = json.dumps({
            "Order_ID": 1
        })

        possible_response1 = "Order successfully deleted"
        possible_response2 = "Order not found"

        # When
        self.app.post('/ordersdb', headers={"Content-Type": "application/json"}, data=payload1)
        response = self.app.delete('/ordersdb', headers={"Content-Type": "application/json"}, data=payload2)

        # Then
        self.assertEqual(possible_response1, response.json['Status'])
        self.assertEqual(response.status_code, 200)

        # When
        response = self.app.delete('/ordersdb', headers={"Content-Type": "application/json"}, data=payload2)

        self.assertEqual(possible_response2, response.json['Status'])
        self.assertEqual(response.status_code, 200)
        self.api.clear_db()

    def cleanUp(self):
        '''Test cleanup'''
        self.api.clear_db()

if __name__ == '__main__':
    unittest.main()

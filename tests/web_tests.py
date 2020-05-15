import unittest
from flask_testing import TestCase
from flask import json
from app import settings
from app.helpers import files as files_helper
from app.models.train_model import train
import os
import random

path_to_train_dataset = os.path.abspath(__file__ + "/../../data/raw/training.csv")

version_number = random.randint(888, 999)
version_id = "v" + str(version_number)


class WebTests(TestCase):
    loaded_app = None

    # flask_testing requires a method called create_app
    def create_app(self):

        if WebTests.loaded_app is None:

            # makes a dummy model just for testing
            train(path_to_train_dataset, version_id)

            # must import the app after the dummy model has been trained
            # because the app loads the models as soon as it's imported

            from app.app import app
            app.testing = True
            WebTests.loaded_app = app
            return app
        else:
            return WebTests.loaded_app

    # we just need a single trained model for all tests
    @classmethod
    def tearDownClass(cls):
        path_to_model = settings.MODELS_ROOT + "/" + files_helper.make_filename(version_id)
        os.remove(path_to_model)

    def test_positive_healthcheck(self):

        route = "/v{}/healthcheck".format(version_number)

        response = self.client.get(route)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.data,'utf-8'), "OK")

    def test_negative_healthcheck(self):
        route = "/v{}/healthcheck".format(version_number + 1)

        response = self.client.get(route)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.data,'utf-8'), "Not OK")

    def test_prediction(self):

        collection = {
            "id": "NG-01",
            "manufacturer": 'toyota',
            "year": 2019,
            "mileage": 10000,
            "sec_status": 'new'
        }

        route = "/v{}/predict".format(version_number)

        response = self.client.post(route, data=json.dumps(collection),
                                    headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 200)

        expected_response = json.dumps({"id": "NG-01", "prediction": 2000000}).replace(" ","")

        actual_response = str(response.data,'utf-8').strip()

        self.assertEqual(actual_response, expected_response)

    def test_400(self):
        # missing manufacturer
        collection = {
           "id": "NG-01",
            "year": 2019,
            "mileage": 10000,
            "sec_status": 'new'
        }

        route = "/v{}/predict".format(version_number)

        response = self.client.post(route, data=json.dumps(collection),
                                    headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)

    def test_404(self):
        collection = {
            "id": "NG-01",
            "year": 2019,
            "mileage": 10000,
            "sec_status": 'new'
        }

        route = "/v{}/predict".format(version_number + 1)

        response = self.client.post(route, data=json.dumps(collection),
                                    headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

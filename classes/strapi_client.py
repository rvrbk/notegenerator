import requests, json, os
from dotenv import load_dotenv

load_dotenv()

class StrapiClient:
    def __init__(self):
        response = requests.post(os.environ.get('STRAPI_URL') + '/api/auth/local', data=json.dumps({'identifier': os.environ.get('STRAPI_IDENTIFIER'), 'password': os.environ.get('STRAPI_PASSWORD')}), headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            self.jwt = response.json()['jwt']
        else:
            print('Error occurred:', response.status_code)

    def post(self, endpoint, data={}):
        response = requests.post(os.environ.get('STRAPI_URL') + endpoint, data=json.dumps(data), headers={'Authorization': 'Bearer {}'.format(self.jwt), 'Content-Type': 'application/json'})

        if response.status_code == 200:
            return True
        
        print('Error occurred:', response.status_code)

    def get(self, endpoint, filters={}):
        response = requests.get(os.environ.get('STRAPI_URL') + endpoint, params=filters, headers={'Authorization': 'Bearer {}'.format(self.jwt), 'Content-Type': 'application/json'})

        if response.status_code == 200:
            return response.json()['data']
        
        print('Error occurred:', response.status_code)
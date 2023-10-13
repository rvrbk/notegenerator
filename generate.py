from datetime import datetime
from dotenv import load_dotenv
import requests, openai, os, json, base64

load_dotenv()

openai.api_key = os.environ.get('OPEN_AI_API_KEY')

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


class JiraClient:
    def get(query):
        auth = (os.environ.get('JIRA_USERNAME'), os.environ.get('JIRA_API_TOKEN'))

        response = requests.get(os.environ.get('JIRA_URL') + '/rest/api/2/search', params={'jql': query}, headers={'Content-Type': 'application/json'}, auth=auth)
        
        if response.status_code == 200:
            return response.json()['issues']
        
        print('Error occurred:', response.status_code)

class StoryMapper:
    def map(data):
        pass

class JiraStoryMapper(StoryMapper):
    def map(data):
        mapped = []
        for field in data:
            mapped.append(Item(field['key'], field['fields']['description']))
        
        return mapped

class Item:
    def __init__(self, key, content):
        self.key = key
        self.content = content

    def __str__(self):
        return '{}, {}'.format(self.key, self.content)

class StoryController:
    def getStoriesByQuery(query):
        pass

class JiraStoryController(StoryController):
    def getStoriesByQuery(query):
        return JiraClient.get(query)
    
class DevOpsStoryController(StoryController):
    def getStoriesByQuery(query):
        pass

class Releasenote:
    def __init__(self, input):
        self.input = input

    def generate(self):
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            messages = [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'GPT, please create user-friendly release notes for the following update, focusing on the new features and enhancements. Ignore the sections on \'Acceptance\', \'How to test\', and any other technical details: {}.'.format(item.content)},
                {'role': 'user', 'content': 'Respond in json format with keys for \'notes\', \'title\', \'tags\' and \'type\', tags can be a comma seperated string, type can be either \'technical\' or \'regular\''},
                {'role': 'user', 'content': 'Assume a non-technical audience and do not put the update or equivalent in the titles'}
            ],
            temperature = 0.7
        )

        return json.loads(response.choices[0].message.content.strip())
    
if __name__ == '__main__':
    strapi = StrapiClient()

    items = JiraStoryMapper.map(JiraStoryController.getStoriesByQuery('fixVersion = {} and type not in (Bug) order by createdDate'.format(os.environ.get('RELEASE'))))
    
    for item in items:
        releasenote = Releasenote(item.content)

        releasenotes = releasenote.generate()
    
        if strapi.post('/api/releasenotes', {'data': {
            'Title': releasenotes['title'],
            'Content': releasenotes['notes'],
            'Release': os.environ.get('RELEASE'),
            'ExternalID': item.key,
            'Created': datetime.now().isoformat()
        }}):
            print('Generated note for {}'.format(item.key))

        






# def get_devops_items():
#     organization = 'netivity'
#     project = 'Core-Portal'
#     team = 'Core-Portal Team'
#     token = os.environ.get('DEVOPS_PAT')
#     token_bytes = f'{token}:'.encode('ascii')
#     encoded_token = base64.b64encode(token_bytes).decode('ascii')
    
#     url = 'https://dev.azure.com/{}/{}/{}/_apis/wit/wiql?api-version=5.0'.format(organization, project, team)
    
#     headers = {
#         'Authorization': f'Basic {encoded_token}',
#         'Content-Type': 'application/json'
#     }

#     response = requests.post(url, headers=headers, json={"query": "select [Custom.Context] from workitems where System.Id = 150718"})

#     if response.status_code == 200:
#         work_item = response.json()
#         return json.dumps(work_item)
#     else:
#         print("Error: {}".format(response.status_code))
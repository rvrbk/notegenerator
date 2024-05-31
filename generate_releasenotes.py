from datetime import datetime
from dotenv import load_dotenv
import os

from classes.strapi_client import StrapiClient
from classes.jira_story_mapper import JiraStoryMapper
from classes.jira_story_controller import JiraStoryController
from classes.releasenote import Releasenote

load_dotenv()

if __name__ == '__main__':
    failed = []

    strapi = StrapiClient()

    items = JiraStoryMapper.map(JiraStoryController.getStoriesByQuery(os.environ.get('QUERY')))
    
    for item in items:
        releasenote = Releasenote(item.content)

        releasenotes = releasenote.generate()
        
        if releasenote and releasenotes:
            if strapi.post('/api/releasenotes', {'data': {
                'Title': releasenotes['title'],
                'Content': releasenotes['notes'],
                'Release': os.environ.get('RELEASE'),
                'ExternalID': item.key,
                'Created': datetime.now().isoformat()
            }}):
                print('Generated note for {}'.format(item.key))
                failed.append(item.key)
        else:
            print('Failed to generate note for {}'.format(item.key))

    if failed
        print('Failed items:')
        print(failed)

        






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

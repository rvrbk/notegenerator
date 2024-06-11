from datetime import datetime
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import os, requests, json

from classes.strapi_client import StrapiClient
from classes.jira_story_mapper import JiraStoryMapper
from classes.devops_story_mapper import DevOpsStoryMapper
from classes.jira_story_controller import JiraStoryController
from classes.devops_story_controller import DevOpsStoryController
from classes.releasenote import Releasenote

load_dotenv()

if __name__ == '__main__':
    failed = []

    strapi = StrapiClient()

    if os.environ.get("MODE") == "JIRA":
        items = JiraStoryMapper.map(JiraStoryController.getStoriesByQuery(os.environ.get('QUERY')))
    elif os.environ.get("MODE") == "DEVOPS":
        items = DevOpsStoryMapper.map(DevOpsStoryController.getStoriesByQuery(os.environ.get('QUERY')))    
    
    for item in items:
        releasenote = Releasenote(item.content)
        
        releasenotes = releasenote.generate()
        
        if releasenote and releasenotes: 
            if strapi.post('/api/releasenotes', {'data': {
                'Title': releasenotes['title'],
                'Content': releasenotes['notes'],
                'Release': os.environ.get('RELEASE'),
                'ExternalID': str(item.key),
                'Created': datetime.now().isoformat()
            }}):
                print('Generated note for {}'.format(item.key))
                
                if os.environ.get("MODE") == "DEVOPS":
                    response = requests.patch(f'https://dev.azure.com/{os.environ.get("DEVOPS_ORGANIZATION")}/_apis/wit/workitems/{str(item.key)}/?api-version=6.0', headers={ 'Content-Type': 'application/json-patch+json' }, auth=HTTPBasicAuth('', os.environ.get('DEVOPS_PAT')), data=json.dumps([{
                        "op": "add",
                        "path": "/fields/Custom.ReleasenoteTitle",
                        "value": releasenotes["title"]
                    },{
                        "op": "add",
                        "path": "/fields/Custom.Releasenote",
                        "value": releasenotes["notes"]
                    }]))
                    
                    if response.status_code == 200:
                        print('Generated devops note for {}'.format(item.key))
                        
            else:
                print('Failed to generate note for {}'.format(item.key))
                failed.append(item.key)
            
        else:
            print('Failed to generate note for {}'.format(item.key))
            failed.append(item.key)
    if failed:
        print('Failed items:')
        print(failed)
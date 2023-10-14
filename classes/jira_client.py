import os, requests
from dotenv import load_dotenv

load_dotenv()

class JiraClient:
    def get(query):
        auth = (os.environ.get('JIRA_USERNAME'), os.environ.get('JIRA_API_TOKEN'))

        response = requests.get(os.environ.get('JIRA_URL') + '/rest/api/2/search', params={'jql': query}, headers={'Content-Type': 'application/json'}, auth=auth)
        
        if response.status_code == 200:
            return response.json()['issues']
        
        print('Error occurred:', response.status_code)
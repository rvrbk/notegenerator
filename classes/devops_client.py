import os, requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

class DevOpsClient:
    def get(query):
        response = requests.post(os.environ.get('DEVOPS_URL'), json={ "query": query }, auth=HTTPBasicAuth('', os.environ.get('DEVOPS_PAT')))

        if response.status_code == 200:
            items = response.json()
            
            ids = []
            for item in items["workItems"]:
                ids.append(item["id"])
        
            detail_response = requests.get(f'https://dev.azure.com/{os.environ.get("DEVOPS_ORGANIZATION")}/_apis/wit/workitems?ids={",".join(map(str, ids))}&api-version=6.0', headers={ 'Content-Type': 'application/json' }, auth=HTTPBasicAuth('', os.environ.get('DEVOPS_PAT')))
        
            return detail_response.json()
        
        print('Error occurred:', response.status_code)
from classes.strapi_client import StrapiClient
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import os, requests, json

if __name__ == '__main__':
    strapi = StrapiClient()

    notes = strapi.get('/api/releasenotes', {
        'filters[Release]': os.environ.get('RELEASE')
    })

    md = '# Release {}\n\n'.format(os.environ.get('RELEASE'))

    for note in notes:
        md += '### {} ({})\n{}\n\n'.format(note['attributes']['Title'], note['attributes']['ExternalID'], note['attributes']['Content'])

    if os.environ.get("MODE") == "JIRA":
        with open('releasenotes_{}.md'.format(os.environ.get('RELEASE')), 'w') as file:
            file.write(md)
    elif os.environ.get("MODE") == "DEVOPS":
        response = requests.put(f"https://dev.azure.com/{os.environ.get('DEVOPS_ORGANIZATION')}/{os.environ.get('DEVOPS_PROJECT')}/_apis/wiki/wikis/{os.environ.get('DEVOPS_WIKI_ID')}/pages?path=Releasenotes for {os.environ.get('RELEASE')}&api-version=6.0", auth=HTTPBasicAuth('', os.environ.get('DEVOPS_PAT')), headers={
            "Content-Type": "application/json"
        }, data=json.dumps({
            "content": md
        }))
        
        if response.status_code == 201:
            print(f"Releasnotes for {os.environ.get('RELEASE')} successfully generated in DevOps")
        else:
            print(response.json())
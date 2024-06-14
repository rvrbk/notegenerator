from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import os, requests, json

from classes.jira_story_mapper import JiraStoryMapper
from classes.devops_story_mapper import DevOpsStoryMapper
from classes.jira_story_controller import JiraStoryController
from classes.devops_story_controller import DevOpsStoryController
from classes.releasenote import Releasenote

from libraries.notes_library import NotesLibrary

load_dotenv()

import argparse

def generate():
    notes_library = NotesLibrary()
    notes_library.create_notes_table()
    
    failed = []

    if os.environ.get("MODE") == "JIRA":
        items = JiraStoryMapper.map(JiraStoryController.getStoriesByQuery(os.environ.get('QUERY')))
    elif os.environ.get("MODE") == "DEVOPS":
        items = DevOpsStoryMapper.map(DevOpsStoryController.getStoriesByQuery(os.environ.get('QUERY')))    
    
    for item in items:
        releasenote = Releasenote(item.content)    
        releasenotes = releasenote.generate()
        
        if releasenote and releasenotes: 
            notes_library = NotesLibrary()
            result = notes_library.insert_note(item, releasenotes)
            
            if result:
                print('Generated note for {}'.format(item.key))
                        
            else:
                print('Failed to generate note for {}'.format(item.key))
                failed.append(item.key)
            
        else:
            print('Failed to generate note for {}'.format(item.key))
            failed.append(item.key)
    if failed:
        print('Failed items:')
        print(failed)

def write():
    notes_library = NotesLibrary()
    notes = notes_library.get_notes(os.environ.get('RELEASE', 'default_release'))

    md = '# Release {}\n\n'.format(os.environ.get('RELEASE'))

    for note in notes:
        md += '### {} ({})\n{}\n\n'.format(note['title'], note['external_id'], note['content'])

    if os.environ.get("MODE") == "JIRA":
        with open('notes/releasenotes_{}.md'.format(os.environ.get('RELEASE')), 'w') as file:
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

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")

subparser.add_parser("generate")
subparser.add_parser("write")

args = parser.parse_args()

if args.command == "generate":
    generate()
elif args.command == "write":
    write()
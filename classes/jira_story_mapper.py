from classes.story_mapper import StoryMapper
from classes.item import Item
import os

class JiraStoryMapper(StoryMapper):
    def map(data):
        mapped = []
        for field in data:
            for storyfield in os.environ.get("CONTEXT_FIELD_PRIO").split(","):
                if storyfield.strip() in field['fields']:
                    mapped.append(Item(field['key'], field['fields'][storyfield.strip()]))
                    break
                    
        
        return mapped
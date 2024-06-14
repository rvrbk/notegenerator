from classes.story_mapper import StoryMapper
from classes.item import Item
import os

class DevOpsStoryMapper(StoryMapper):
    def map(data):
        mapped = []
        for field in data["value"]:
            for storyfield in os.environ.get("CONTEXT_FIELD_PRIO").split(","):
                if storyfield.strip() in field['fields']:
                    mapped.append(Item(field['id'], field['fields'][storyfield.strip()]))
                    break
                
        print(mapped[0])
                        
        return mapped
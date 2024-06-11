from classes.story_mapper import StoryMapper
from classes.item import Item

class DevOpsStoryMapper(StoryMapper):
    def map(data):
        mapped = []
        for field in data["value"]:
            if 'Custom.Context' in field['fields']:
                mapped.append(Item(field['id'], field['fields']['Custom.Context']))
            elif 'System.Description' in field['fields']:
                mapped.append(Item(field['id'], field['fields']['System.Description']))
        
        return mapped
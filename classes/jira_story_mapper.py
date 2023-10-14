from classes.story_mapper import StoryMapper
from classes.item import Item

class JiraStoryMapper(StoryMapper):
    def map(data):
        mapped = []
        for field in data:
            mapped.append(Item(field['key'], field['fields']['description']))
        
        return mapped
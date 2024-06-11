from classes.story_controller import StoryController
from classes.devops_client import DevOpsClient

class DevOpsStoryController(StoryController):
    def getStoriesByQuery(query):
        return DevOpsClient.get(query)
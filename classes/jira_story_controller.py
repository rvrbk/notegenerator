from classes.story_controller import StoryController
from classes.jira_client import JiraClient

class JiraStoryController(StoryController):
    def getStoriesByQuery(query):
        return JiraClient.get(query)
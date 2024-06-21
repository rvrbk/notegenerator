import openai, os, json
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('OPEN_AI_API_KEY')
openai.api_type = os.environ.get('OPEN_AI_API_TYPE')
openai.api_base = os.environ.get('OPEN_AI_API_BASE')
openai.api_version = os.environ.get('OPEN_AI_API_VERSION')

class Releasenote:
    def __init__(self, input):
        self.input = input

    def generate(self):
        try:
            response = openai.ChatCompletion.create(
                engine = 'chat',
                model = os.environ.get("OPEN_AI_API_MODEL", "gpt-4"),
                messages = [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': 'GPT, please create user-friendly release notes for the following update, focusing on the new features and enhancements. Ignore the sections on \'Acceptance\', \'How to test\', and any other technical details: {}.'.format(self.input)},
                    {'role': 'user', 'content': 'Respond in json format with keys for \'notes\', \'title\', \'tags\' and \'type\', tags can be a comma seperated string, type can be either \'technical\' or \'regular\''},
                    {'role': 'user', 'content': 'Assume a non-technical audience and do not put the update or equivalent in the titles'}
                ],
                temperature = 0.7
            )
            
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            return False
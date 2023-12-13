from classes.strapi_client import StrapiClient
from dotenv import load_dotenv
import os, markdown, json, requests

if __name__ == '__main__':
    strapi = StrapiClient()

    notes = strapi.get('/api/releasenotes', {
        'filters[Release]': os.environ.get('RELEASE')
    })

    md = '<h1>Release {}</h1><br>'.format(os.environ.get('RELEASE'))

    for note in notes:
        md += '<h2>{} (<a href=\'{}\' target=\'_blank\'>{}</a>)</h2>{}<br><br>'.format(note['attributes']['Title'], os.environ.get('RELEASE').format(note['attributes']['ExternalID']), note['attributes']['ExternalID'], note['attributes']['Content'])

    response = requests.post(
        os.environ.get('TEAMS_WEBHOOK'),
        data=json.dumps({
            '@type': 'MessageCard',
            '@context': 'http://schema.org/extensions',
            'text': markdown.markdown(md)
        }),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print('Failed to send message')
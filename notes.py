from classes.strapi_client import StrapiClient
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    strapi = StrapiClient()

    notes = strapi.get('/api/releasenotes', {
        'filters[Release]': os.environ.get('RELEASE')
    })

    md = '# Release {}\n\n'.format(os.environ.get('RELEASE'))

    for note in notes:
        md += '### {}\n{}\n\n'.format(note['attributes']['Title'], note['attributes']['Content'])

    with open('external_releasenotes_{}.md'.format(os.environ.get('RELEASE')), 'w') as file:
        file.write(md)
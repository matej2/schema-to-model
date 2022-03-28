import re
import sys

from django.conf import settings

settings.configure()

from dr_scaffold.generators import Generator
from schemaorg.main import Schema

schema_name = 'Restaurant'
schema = Schema(schema_name)
toadd = []

TYPE_MAPPINGS = {
    'Text': 'CharField',
    'Number': 'SmallIntegerField',
    'Integer': 'IntegerField',
    'URL': 'URLField',
    'DateTime': 'DateTimeField',
    'Date': 'DateTimeField',
    'Boolean': 'BooleanField'
}

def get_mapping(entity):
    try:
        return TYPE_MAPPINGS[entity]
    except KeyError:
        return 'CharField'

def url_to_entity(url):
    ent = re.sub(r'^.+\/', '', url, flags=re.IGNORECASE)
    return re.sub(r'\W', '', ent, flags=re.IGNORECASE)

#schema_name = ''

#if len(sys.argv) > 0:
#    schema_name = sys.argv[0]

for name, meta in schema._properties.items():
    entity = url_to_entity(meta['rangeIncludes'])
    toadd.append(f'{name}:{get_mapping(entity)}')


gen = Generator('test', schema_name, toadd, False, False)
gen.run()

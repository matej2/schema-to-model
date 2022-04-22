import re
import sys

from django.conf import settings

settings.configure()

from dr_scaffold.generators import Generator
from schemaorg.main import Schema

schema_name = 'Restaurant'

TYPE_MAPPINGS = {
    'Text': 'CharField',
    'Number': 'SmallIntegerField',
    'Integer': 'IntegerField',
    'URL': 'URLField',
    'DateTime': 'DateTimeField',
    'Date': 'DateTimeField',
    'Boolean': 'BooleanField'
}

def is_entity_in_mapping(entity):
    animals.index('dog')

def get_mapping(entity):
    try:
        return TYPE_MAPPINGS[entity]
    except KeyError:
        return entity

def url_to_entity(url):
    ent = re.sub(r'^.+\/', '', url, flags=re.IGNORECASE)
    return re.sub(r'\W', '', ent, flags=re.IGNORECASE)

#schema_name = ''

#if len(sys.argv) > 0:
#    schema_name = sys.argv[0]

def get_generator_list(name, lvl=2):
    schema = Schema(schema_name)
    toadd = []
    items = schema._properties.items()
    subobjects = []
    # TODO: Replace with recursion
    # Get sub objects first
    for name, meta in items:
        entity = url_to_entity(meta['rangeIncludes'])
        if entity not in TYPE_MAPPINGS && lvl > 0:
            lvl = lvl - 1
            get_generator_list(entity, lvl)
        else:
            toadd.append(f'{name}:{get_mapping(entity)}')
        

add_list = get_generator_list(schema_name)
gen = Generator('test', schema_name, add_list, False, False)
gen.run()

import re
import sys

from django.conf import settings

settings.configure()

from dr_scaffold.generators import Generator
from schemaorg.main import Schema

origin_name = 'Book'

TYPE_MAPPINGS = {
    'Text': 'CharField',
    'Number': 'SmallIntegerField',
    'Integer': 'IntegerField',
    'URL': 'URLField',
    'DateTime': 'DateTimeField',
    'Date': 'DateTimeField',
    'Boolean': 'BooleanField',
    'Place': 'CharField',
    'Brand': 'CharField',
    'ImageObject': 'ImageField',
    'Thing': 'CharField'
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


def generate_model(schema_name, lvl=2):
    schema = Schema(schema_name)
    toadd = []
    items = schema._properties.items()
    # TODO: Replace with recursion
    # Get sub objects first
    for name, meta in items:
        entity = url_to_entity(meta['rangeIncludes'])
        if entity not in TYPE_MAPPINGS and lvl > 0:
            lvl = lvl - 1
            print(f'Go into {name}:{entity}')
            generate_model(entity, lvl)
            toadd.append(f'{name}_{entity}:foreignkey:{entity}')
        else:
            toadd.append(f'{name}:{get_mapping(entity)}')
            print(f'Append {name}')
    gen = Generator('test', schema_name, toadd, False, False)
    gen.run()


generate_model(origin_name)

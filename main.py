import re
import sys

from django.conf import settings

settings.configure()

from dr_scaffold.generators import Generator
from schemaorg.main import Schema

origin_schema_name = 'MonetaryGrant'

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
    'Thing': 'CharField',
    'Action': 'CharField'
}

generated = []


def get_mapping(entity):
    try:
        return TYPE_MAPPINGS[entity]
    except KeyError:
        return 'CharField'


def url_to_entity(url):
    ent = re.sub(r'^.+\/', '', url, flags=re.IGNORECASE)
    return re.sub(r'\W', '', ent, flags=re.IGNORECASE)


def generate_model(schema_name, lvl=1):
    schema = Schema(schema_name)
    toadd = []
    toadd_line = []
    items = schema._properties.items()
    # TODO: Replace with recursion
    # Get sub objects first
    for name, meta in items:
        entity = url_to_entity(meta['rangeIncludes'])
        if entity not in TYPE_MAPPINGS and lvl > 0:
            print(f'Go into {name}:{entity}, lvl {lvl}')
            if entity not in generated:
                generated.append(entity)
                print(f'{entity} not generated')
                generate_model(entity, int(lvl)-1)
            toadd.append(f'{name}_{entity}:foreignkey:{entity}')
        else:
            toadd.append(f'{name}:{get_mapping(entity)}')
            print(f'Append {name}')
    gen = Generator('test', schema_name, toadd, False, False)
    gen.run()


generate_model(origin_schema_name)

import re
import sys

from django.conf import settings

settings.configure()

from dr_scaffold.generators import Generator
from schemaorg.main import Schema

origin_schema_name = 'Mountain'

TYPE_MAPPINGS = {
    'Text': 'CharField',
    'Number': 'SmallIntegerField',
    'Integer': 'IntegerField',
    'URL': 'URLField',
    'DateTime': 'DateTimeField',
    'Time': 'TimeField',
    'Date': 'DateTimeField',
    'Boolean': 'BooleanField',
    'Place': 'CharField',
    'Brand': 'CharField',
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


def is_substring_in_list(sub, list):
    for str in list:
        if sub in str:
            return True


def generate_model(schema_name, lvl=1):
    schema = Schema(schema_name)
    toadd = []
    items = schema._properties.items()
    # TODO: Replace with recursion
    # Get sub objects first
    for name, meta in items:
        entity = url_to_entity(meta['rangeIncludes'])
        if entity not in TYPE_MAPPINGS and lvl > 0:
            print(f'{entity} -> {name}, lvl {lvl}')
            if entity not in generated:
                print(f'Generating {entity}')
                generate_model(entity, int(lvl)-1)
                generated.append(entity)
            if entity == schema_name:
                toadd.append(f'{name}_{entity}:foreignkey:"self"')
            # Temp fix to avoid reverse accessors
            elif is_substring_in_list(entity, toadd):
                toadd.append(f'{name}_{entity}:CharField')
            else:
                toadd.append(f'{name}_{entity}:foreignkey:{entity}')
        else:
            toadd.append(f'{name}:{get_mapping(entity)}')
    gen = Generator('test', schema_name, toadd, False, False)
    gen.run()


generate_model(origin_schema_name)

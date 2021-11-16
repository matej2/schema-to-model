import re
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Test.settings")
django.setup()
from dr_scaffold.generators import Generator
from schemaorg.main import Schema
from schemaorg.utils import read_yaml, write_yaml


recipe = read_yaml('empty.yml')
schema_name = 'Article'
schema = Schema(schema_name)

TYPE_MAPPINGS = {
    'Text': 'CharField'
}

def get_mapping(entity):
    try:
        return TYPE_MAPPINGS[entity]
    except KeyError:
        return 'CharField'

def url_to_entity(url):
    ent = re.sub(r'^.+\/', '', url, flags=re.IGNORECASE)
    return re.sub(r'\W', '', ent, flags=re.IGNORECASE)

toadd = []
for name, meta in schema._properties.items():
    entity = url_to_entity(meta['rangeIncludes'])
    toadd.append(f'{name}:{get_mapping(entity)}')

print(toadd)

gen = Generator('test', schema_name, toadd, False, False)
gen.run()

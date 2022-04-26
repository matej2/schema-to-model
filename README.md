# Schema-to-model
Genrates models based on Schema.org definitions.

The idea for an this app is that it would read pre-defined data structures (schema vocabularies) and generate models based on that. The best thing is that it would also generate all successors. For example: For Article it would generate Author, Category, Publisher... Maybe this app is not the best way to develop, but it is a way to kickstart it.

Technical details: Application will get schema information from schema.org. It will then use https://github.com/Abdenasser/dr_scaffold to generate objects. Later, I also plan to make generators for other languages

## Instructions to use

On first run, execute `Pipenv install`
1. Open `main.py` and edit `origin_schema_name`
2. `echo "python main.py" | pipenv shell`
4. Temp fix: `cp test/migrations/__init__.py test/__init__.py && sed -i -r -e 's/(max_length=[0-9]+)\)/\1, null=True, blank=True)/g' test/models.py && sed -i -r -e 's/\((null=True)\)/(\1, blank=True)/g' test/models.py`
5. `echo "python manage.py makemigrations && python manage.py migrate" | pipenv shell`
6. (Optional) `echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')" | python manage.py shell`
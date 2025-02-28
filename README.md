# Schema-to-Model

Generates models based on Schema.org definitions.

This application is designed to read predefined data structures (schema vocabularies) and automatically generate models from them. A key feature is its ability to generate all related successor models. For example, for an `Article`, it would generate associated models such as `Author`, `Category`, `Publisher`, and more. While this approach may not be the most conventional for development, it serves as an excellent way to kickstart projects by automating the creation of foundational models.

---

## Technical Details

The application retrieves schema information from [Schema.org](https://schema.org) and uses the [dr_scaffold](https://github.com/Abdenasser/dr_scaffold) library to generate Django models. Future plans include extending the functionality to support model generation for other programming languages.

---

## Instructions for Use

1. On the first run, install dependencies:
```bash
pipenv install
```

2. Open `main.py` and edit the `origin_schema_name` variable to specify the desired schema.

3. Run the script to generate models:
```bash
echo "python main.py" | pipenv shell
```

4. Apply a temporary fix to the generated models (optional but recommended):
```bash
cp test/migrations/__init__.py test/__init__.py && sed -i -r -e 's/(max_length=[0-9]+)\)/\1, null=True, blank=True)/g' test/models.py && sed -i -r -e 's/\((null=True)\)/(\1, blank=True)/g' test/models.py && sed -i -r -e 's/\(\)/(null=True, blank=True)/g' test/models.py
```

5. Create and apply database migrations:
```bash
echo "python manage.py makemigrations && python manage.py migrate" | pipenv shell
```

6. (Optional) Create a superuser for Django admin access:
```bash
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')" | python manage.py shell
```

---

This tool is ideal for developers looking to quickly bootstrap their projects with structured, schema-based models while minimizing manual setup.

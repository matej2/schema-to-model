import factory

from core_dir.blog.models import Author


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    def __new__(cls, *args, **kwargs):
        return super().__new__(*args, **kwargs)


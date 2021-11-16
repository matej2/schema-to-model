import pytest
from factories import AuthorFactory


@pytest.mark.django_db
def test_author_factory():
    instance = AuthorFactory()
    assert instance.id


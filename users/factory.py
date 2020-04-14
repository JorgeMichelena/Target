import factory
from factory.django import DjangoModelFactory as Factory
from factory.faker import faker
from users.models import User


class UserFactory(Factory):
    class Meta:
        model = User

    pk = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    first_name = faker.Faker().first_name()
    last_name = faker.Faker().last_name()
    password = faker.Faker().password()

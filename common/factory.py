import factory
import random


class TransactionFactory(factory.django.DjangoModelFactory):
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=0, positive=True)
    type = factory.Faker('pyint', min_value=1, max_value=3)

    class Meta:
        model = 'student.Transaction'


class StudentFactory(factory.django.DjangoModelFactory):
    full_name = factory.Faker('name')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    email = factory.Faker('ascii_company_email')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=6, maximum_age=25)

    class Meta:
        model = 'student.Student'

    @factory.post_generation
    def create_docs(self, create, extracted, **kwargs):
        if create:
            TransactionFactory.create_batch(5, student=self)


class TariffFactory(factory.django.DjangoModelFactory):
    title = factory.LazyAttribute(lambda x: f"T {random.randint(1, 25)}")
    price = factory.Faker('pydecimal', left_digits=6, right_digits=0, positive=True)

    class Meta:
        model = 'organization.Tariff'


class GroupFactory(factory.django.DjangoModelFactory):
    title = factory.LazyAttribute(lambda x: f"G  {random.randint(1, 12)}-{random.choice(('A', 'B', 'C','D','F','G'))}")

    class Meta:
        model = 'organization.Group'


class TeacherFactory(factory.django.DjangoModelFactory):
    full_name = factory.Faker('name')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    email = factory.Faker('ascii_company_email')

    class Meta:
        model = 'organization.Teacher'


class OrganizationFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('company')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    email = factory.Faker('ascii_company_email')
    balance = factory.Faker('pydecimal', left_digits=4, right_digits=2)

    class Meta:
        model = 'organization.Organization'

    @factory.post_generation
    def create_docs(self, create, extracted, **kwargs):
        if create:
            for i in range(0, random.randint(3, 11)):
                teacher = TeacherFactory.create(organization=self)
                tariff = TariffFactory.create(organization=self)
                group = GroupFactory.create(organization=self, teacher=teacher, tariff=tariff)
                if random.choice((True, False, True, True, True, True)):
                    tariff = None
                StudentFactory.create_batch(random.randint(12, 21), group=group, tariff=tariff)
            if not self.parent_id:
                OrganizationFactory.create_batch(random.randint(0, 6), parent=self)

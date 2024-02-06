from django.test import TestCase
from .models import Insurance, InsuranceDetail, InsuredPerson

class InsuranceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Insurance.objects.create(insurance_name='Test Insurance')

    def test_insurance_name_label(self):
        insurance = Insurance.objects.get(id=1)
        field_label = insurance._meta.get_field('insurance_name').verbose_name
        self.assertEqual(field_label, 'Insurance')

    def test_insurance_name_max_length(self):
        insurance = Insurance.objects.get(id=1)
        max_length = insurance._meta.get_field('insurance_name').max_length
        self.assertEqual(max_length, 80)

class InsuranceDetailModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        InsuranceDetail.objects.create(detail_title='Test Detail')

    def test_detail_title_label(self):
        detail = InsuranceDetail.objects.get(id=1)
        field_label = detail._meta.get_field('detail_title').verbose_name
        self.assertEqual(field_label, 'Insurance Detail')

    def test_detail_title_max_length(self):
        detail = InsuranceDetail.objects.get(id=1)
        max_length = detail._meta.get_field('detail_title').max_length
        self.assertEqual(max_length, 30)

class InsuredPersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_insurance = Insurance.objects.create(insurance_name='Test Insurance')
        test_person = InsuredPerson.objects.create(
            first_name='Test',
            last_name='Person',
            age='30',
            address='Test Address',
            insurance=test_insurance
        )
        test_detail = InsuranceDetail.objects.create(detail_title='Test Detail')
        test_person.detail_insurance.add(test_detail)

    def test_first_name_label(self):
        person = InsuredPerson.objects.get(id=1)
        field_label = person._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'First Name')

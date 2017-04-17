from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from model_mommy import mommy

from core.views import DatatablesListView
from .models import TestPerson


class TestDatatablesListView(TestCase):
    """
    Author: Milton Lenis
    Date: 16 April 2017
    TestCase for the DatatablesListView view, this tests all of the insider methods of the view
    """

    def setUp(self):
        self.view = DatatablesListView()
        mommy.make_recipe('tests.test_person', _quantity=10)

    def tearDown(self):
        del self.view

    def test_get_queryset(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Test for the 'get_queryset' method of the view
        """
        tested_method = self.view.get_queryset
        # First the exception is checked because the view has no model or queryset
        with self.assertRaises(ImproperlyConfigured):
            tested_method()

        self.view.model = TestPerson
        self.assertListEqual(list(tested_method()), list(TestPerson.objects.all()))

        self.view.queryset = TestPerson.objects.filter(gender=1)
        self.assertListEqual(list(tested_method()), list(TestPerson.objects.filter(gender=1)))

    def test_get_field_names(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Test for the 'get_field_names' method of the view
        """
        tested_method = self.view.get_field_names
        # First we test the assertion because the view has no model or fields
        with self.assertRaises(ImproperlyConfigured):
            tested_method()

        self.view.model = TestPerson
        self.assertListEqual(tested_method(), ['id', 'name', 'birth_date', 'gender', 'dog', 'cats'])

        # Let's manually define the fields and test
        self.view.fields = ['name', 'birth_date', 'gender']
        self.assertListEqual(tested_method(), ['name', 'birth_date', 'gender'])

    def test_get_field_instances(self):
        """
        Author: Milton Lenis
        Date 16 April 2017
        Test for the 'get_field_instances' method of the view
        """
        tested_method = self.view.get_field_instances
        self.view.model = TestPerson
        self.view.fields = ['name', 'birth_date', 'gender']
        field_names = [field.name for field in tested_method()]
        self.assertListEqual(field_names, self.view.fields)

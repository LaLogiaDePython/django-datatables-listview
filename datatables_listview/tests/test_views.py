from django.core.exceptions import ImproperlyConfigured
from django.http import QueryDict
from django.test import RequestFactory
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
        self.request = RequestFactory()
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

    def test_get_draw_parameters(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Test for the 'get_draw_parameters' method of the view
        """
        # Add a fake request.GET dict
        self.view.model = TestPerson
        self.request.GET = {
            'start': 5,
            'length': 10,
            'order[0][column]': 3,
            'order[0][dir]': 'desc',
            'search[value]': 'Some search',
            'draw': 1
        }
        method_result = self.view.get_draw_parameters(self.request)
        # Check the type of the result is 'Draw' which is the name of the namedtuple
        self.assertEqual(type(method_result).__name__, 'Draw')
        self.assertEqual(method_result.start, 5)
        # 15 is the start + length
        self.assertEqual(method_result.end, 15)
        # Gender is the third column
        self.assertEqual(method_result.sort_column, 'gender')
        self.assertEqual(method_result.sort_order, 'desc')
        self.assertEqual(method_result.search, 'Some search')
        self.assertEqual(method_result.draw, 1)

    def test_filter_by_search_text(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Test for the 'filter_by_search_text' method of the view
        """
        self.view.model = TestPerson
        self.view.fields = ['name', 'birth_date', 'gender', 'id']
        tested_method = self.view.filter_by_search_text
        # Normal case searching for a unique coincidence
        method_result = tested_method(self.view.get_queryset(), "Name3")
        self.assertEqual(method_result.count(), 1)

        # Case with multiple coincidences because there is "Name1" and "Name10"
        method_result = tested_method(self.view.get_queryset(), "Name1")
        self.assertEqual(method_result.count(), 2)

        # Case-Insensitive search test
        method_result = tested_method(self.view.get_queryset(), "naMe4")
        self.assertEqual(method_result.count(), 1)

        # icontains search tests
        method_result = tested_method(self.view.get_queryset(), "ame")
        self.assertEqual(method_result.count(), 10)
        method_result = tested_method(self.view.get_queryset(), "aMe1")
        self.assertEqual(method_result.count(), 2)

        # Choices display test
        method_result = tested_method(self.view.get_queryset(), "FEMALE")
        # Because the rows are generated with aleatory genders we assertTrue for no exact value
        self.assertTrue(method_result.exists())
        # This will assert on 'MALE' and 'FEMALE' values
        method_result = tested_method(self.view.get_queryset(), "MALE")
        self.assertTrue(method_result.exists())

        # Choices insensitive display test
        method_result = tested_method(self.view.get_queryset(), "FeMale")
        self.assertTrue(method_result.exists())

        # icontains choices display test
        method_result = tested_method(self.view.get_queryset(), "FeMa")
        self.assertTrue(method_result.exists())

from collections import namedtuple

from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse

from .utils import generate_q_objects_by_fields_and_words


class DatatablesListView:
    """
    Author: Milton Lenis
    Date: 16 April 2017
    View implementation for datatables_listview
    """
    model = None
    queryset = None
    fields = None

    def get_queryset(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to get the queryset or generate one with the model
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset.all()

    def get_field_names(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to get the fields definition for this listview, return all of the model fields if the developer doesn't
        setup the fields
        """
        if self.fields is None:
            return [field.name for field in self.model._meta.get_field_names()]
        else:
            return self.fields

    def get_field_instances(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to get all the field instances using the Django's Model _meta API
        """
        field_names = self.get_field_names()
        return [self.model._meta.get_field(field_name) for field_name in field_names]

    def get_draw_parameters(self, request):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to extracting the draw parameters from the request, those parameters are sent by datatables server-side
        """
        # Using namedtuple for readability, the var name is capitalized because this namedtuple is used like a class
        Draw = namedtuple('Draw', ['start', 'end', 'sort_column', 'sort_order', 'search', 'draw'])

        start = int(request.GET.get('start', 0))
        end = start + int(request.GET.get('length', 0))
        sort_column = self.get_field_names()[int(request.GET.get('order[0][column]', 0))]
        sort_order = request.GET.get('order[0][dir]', "")
        search = request.GET.get('search[value]', "")
        draw = int(request.GET.get('draw', 0))

        return Draw(start, end, sort_column, sort_order, search, draw)

    def filter_by_search_text(self, queryset, search_text):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to filter the queryset given a search_text, this filters the queryset by each one of the fields doing
        icontains lookup and spliting the search_text into words
        """
        # First we need to generate Q objects to do the filtering all over the queryset
        q_objects_for_filtering = generate_q_objects_by_fields_and_words(self.get_field_instances(), search_text)
        return queryset.filter(q_objects_for_filtering)

    def filter_by_draw_parameters(self, queryset, draw_parameters):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method ot filter the queryset with the draw parameters, this returns the queryset sorted (Depending of the
        order) by a column and slices the queryset by a start position and end position
        """
        sort_order = ""
        if draw_parameters.sort_order == "desc":
            sort_order = "-"
        sort_criteria = "{0}{1}".format(sort_order, draw_parameters.sort_column)
        return queryset.order_by(sort_criteria)[draw_parameters.start:draw_parameters.end]

    def generate_data(self, request):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to generate the final data required for the JsonResponse, it returns a dictionary with the data
        formated as datatables requires it
        """
        draw_parameters = self.get_draw_parameters(request)
        queryset = self.get_queryset()

        if draw_parameters.search:
            queryset = self.filter_by_search_text(queryset, draw_parameters.search)

        objects_count = queryset.count()
        # This uses the 'filter_by_draw_params' to filter the queryset according with the draw parameters
        # This means: it's the filter for the displaying page of the datatable
        queryset = self.filter_by_draw_parameters(queryset, draw_parameters)
        if self.get_options_list():
            generated_rows = self.generate_rows_with_options()
        else:
            generated_rows = self.generate_rows()
        return {
            'draw': draw_parameters.draw,
            'recordsTotal': objects_count,
            'recodsFiltered': objects_count,
            'data': generated_rows
        }

    def get(self, request, *args, **kwargs):
        """
        Author: Milton Lenis
        Date: April 16 2017
        If the request is ajax it returns the requested data as a JSON, if not, it calls the super to give a normal
        http response and show the template
        """
        if request.is_ajax():
            final_data = self.generate_data(request)
            return JsonResponse(final_data)
        else:
            return super(DatatablesListView, self).get(request, *args, **kwargs)

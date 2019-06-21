from collections import namedtuple

from django.db.models import Q


def generate_q_objects_by_fields_and_words(fields, search_text):
    """
    Author: Milton Lenis
    Date: 16 April 2017
    A handy method to generate Q Objects for filtering the queryset, this
    generates a Q Object by each field with each word, that means, if you have
    a search_term with 3 words and 3 fields this generates 9 Q Objects.

    This also looks if the field has choices, if so, it cast to the choices
    internal representation to do the Q Object creation correctly

    Because Q Objects internally are subclasses of django.utils.tree.Node we can
    'add' Q Objects with connectors,
    see: https://bradmontgomery.net/blog/adding-q-objects-in-django/
    """
    q = Q()
    search_text = search_text.split(" ")
    for field in fields:
        for word in search_text:
            if field.choices:
                # Build a dict with the dictionary to do search by choices
                # display
                # This dictionary takes the value (display of the choices) as
                # key and the internal representation as value
                # TODO: Change this
                field_choices = {value.lower(): key for key, value in field.choices}
                # Search if the searched word exists in the field choices
                value_coincidences = [
                    value for key, value in field_choices.items()
                    if word.lower() in key
                ]
                if value_coincidences:
                    search_criteria = {"%s__in" % field.name: value_coincidences}
                    q.add(
                        Q(**search_criteria),
                        Q.OR
                    )
            else:
                instruction = "%s__icontains" % field.name
                search_criteria = {instruction: word}
                # Adding q objects with OR connector
                q.add(
                    Q(**search_criteria),
                    Q.OR
                )
    return q


def arrayfield_keys_to_values(keys, choices):
    values = []
    for key, value in choices:
        if key in keys:
            values.append(value)
    return values


def create_column_defs_list(column_defs):
    column_defs_list = []
    for counter, column_def in enumerate(column_defs):
        if type(column_def) == str:
            column_defs_list.append({'title': column_def, 'targets': counter, 'orderable': 1, 'searchable': 1})
        elif type(column_def) == dict:
            column_def['targets'] = counter
            column_defs_list.append(column_def)

    return column_defs_list


# Using namedtuple for readability, the var name is capitalized because
# this namedtuple is used like a class
Draw = namedtuple(
    'Draw',
    ['start', 'end', 'sort_column', 'sort_order', 'search', 'draw']
)

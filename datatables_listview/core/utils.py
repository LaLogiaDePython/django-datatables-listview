from django.db.models import Q


def generate_q_objects_by_fields_and_words(fields, search_text):
    """
    Author: Milton Lenis
    Date: 16 April 2017
    A handy method to generate Q Objects for filtering the queryset, this generates a Q Object by each field with each
    word, that means, if you have a search_term with 3 words and 3 fields this generates 9 Q Objects.

    This also looks if the field has choices, if so, it cast to the choices internal representation to do the Q Object
    creation correctly

    Because Q Objects internally are subclasses of django.utils.tree.Node we can 'add' Q Objects with connectors,
    see: https://bradmontgomery.net/blog/adding-q-objects-in-django/
    """
    q = Q()
    search_text = search_text.split(" ")
    for field in fields:
        for word in search_text:
            if field.choices:
                # Build a dict with the dictionary to do search by choices display
                field_choices = {key.lower(): value for key, value in field.choices}
                # Search if the searched word exists in the field choices
                display_to_value = field_choices.get(word.lower(), "")
                if display_to_value:
                    search_criteria = {field.name: display_to_value}
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

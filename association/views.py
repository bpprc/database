from django.shortcuts import render
from association.models import DataModel
from database.models import PesticidalProteinDatabase
import re


def _sorted_nicely(l, sort_key=None):
    """ Sort the given iterable in the way that humans expect. https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/ """
    def convert(text): return int(text) if text.isdigit() else text
    if sort_key is None:
        def alphanum_key(key): return [convert(c)
                                       for c in re.split('([0-9]+)', key)]
    else:
        def alphanum_key(key): return [convert(c) for c in re.split(
            '([0-9]+)', getattr(key, sort_key))]
    return sorted(l, key=alphanum_key)


def data_association_links(request):
    return render(request, 'association/data_association_links.html')


def example_content(request):
    return render(request, 'association/example_content.html')


def data_teams(request):
    return render(request, 'association/data_teams.html')


def list_proteins(request):
    category_endswith1 = []

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name', flat=True).distinct()
    for category in categories:
        if category[-1] == '1' and not category[-2].isdigit():
            category_endswith1.append(category)

    proteins = _sorted_nicely(category_endswith1)

    context = \
        {'proteins': proteins}

    return render(request, 'association/list_proteins.html', context)

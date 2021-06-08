import re
from difflib import get_close_matches

import requests
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from association.forms import SearchForm
from association.models import Association
from database.filter_results import (
    Search,
    filter_one_name,
)
from database.models import PesticidalProteinDatabase


def metadatabase_protein_detail(request, name):

    context = {
        "protein": Association.objects.filter(name=name),
    }

    return render(request, "association/metadatabase_protein_detail.html", context)


def _sorted_nicely(l, sort_key=None):
    """Sort the given iterable in the way that humans expect. https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/"""

    def convert(text):
        return int(text) if text.isdigit() else text

    if sort_key is None:

        def alphanum_key(key):
            return [convert(c) for c in re.split("([0-9]+)", key)]

    else:

        def alphanum_key(key):
            return [convert(c) for c in re.split("([0-9]+)", getattr(key, sort_key))]

    return sorted(l, key=alphanum_key)


def data_association_links(request):
    context = {"items": Association.objects.all()}

    return render(request, "association/data_association_links.html", context)


def display_protein_data(request, name):
    context = {"proteins": Association.objects.filter(name=name)}

    return render(request, "association/display_protein_data.html", context)


def example_content(request):
    return render(request, "association/example_content.html")


def data_teams(request):
    return render(request, "association/data_teams.html")


def search_association(request):
    form = SearchForm()
    return render(request, "association/search_page.html", {"form": form})


def list_proteins(request):
    category_endswith1 = []

    categories = PesticidalProteinDatabase.objects.order_by(
        "name").values_list("name", flat=True).distinct()
    for category in categories:
        if category[-1] == "1" and not category[-2].isdigit():
            category_endswith1.append(category)

    proteins = _sorted_nicely(category_endswith1)

    context = {"proteins": proteins}

    return render(request, "association/list_proteins.html", context)


def search_data_association(request):
    """Returns the results based on the search query."""
    if request.method == "POST":
        form = SearchForm(request.POST)
        proteins = []
        single_digit = False
        if form.is_valid():
            query = form.cleaned_data["search_term"]
            field_type = form.cleaned_data["search_fields"]

            # searches = re.split(r':|, ?|\s |_ |. |; |\n', query)
            searches = re.split(r":|, ?|\s* |\n|;", query)

            if field_type == "pesticidal protein name":
                q_objects = Q()
                q_search = Q()
                for search in searches:
                    if Search(search).is_wildcard():
                        search = search[:-1]
                    else:
                        search = search
                    k = Search(search)
                    if k.is_fullname():
                        q_objects.add(Q(name__iexact=search), Q.OR)
                    if k.is_uppercase():
                        q_objects.add(Q(name__icontains=search), Q.OR)
                    if k.is_lowercase():
                        q_objects.add(Q(name__icontains=search), Q.OR)
                    if k.is_single_digit():
                        single_digit = True
                        q_search.add(Q(name__icontains=search), Q.OR)
                    if k.is_double_digit():
                        q_objects.add(Q(name__icontains=search), Q.OR)
                    if k.is_triple_digit():
                        q_objects.add(Q(name__icontains=search), Q.OR)
                    if k.is_three_letter():
                        q_objects.add(Q(name__icontains=search), Q.OR)
                    if k.is_three_letter_case():
                        q_objects.add(Q(name__icontains=search), Q.OR)
                    else:
                        q_objects.add(Q(name__iexact=search), Q.OR)
                proteins1 = Association.objects.none()
                proteins2 = Association.objects.none()
                if q_objects:
                    proteins1 = Association.objects.filter(q_objects)
                if q_search:
                    proteins2 = Association.objects.filter(q_search)
                if proteins1 and proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = list(proteins1) + proteins2
                    proteins = _sorted_nicely(proteins, sort_key="name")
                elif proteins1:
                    proteins = _sorted_nicely(proteins1, sort_key="name")
                elif proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = _sorted_nicely(proteins2, sort_key="name")

            elif field_type == "target species taxon id":
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(taxonid__icontains=search), Q.OR)

                proteins = Association.objects.filter(q_objects)
                proteins = _sorted_nicely(proteins, sort_key="name")

                if not proteins:
                    words_taxonid = list(
                        set(Association.objects.values_list("taxonid", flat=True)))
                    new_search = []

                    for search in searches:
                        new_search.append(get_close_matches(
                            search, words_taxonid, 1, 0.3))

                    context = {"new_search": new_search}
                    return render(
                        request,
                        "association/search_results.html",
                        context,
                    )

            elif field_type == "target species":
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(target_species__icontains=search), Q.OR)

                proteins = Association.objects.filter(q_objects)
                proteins = _sorted_nicely(proteins, sort_key="name")

                if not proteins:
                    species = list(
                        set(Association.objects.values_list("target_species", flat=True)))
                    words_target_species = [
                        i.split(" ", 1)[0] for i in species]
                    new_search = []

                    for search in searches:
                        new_search.append(get_close_matches(
                            search, words_target_species, 1, 0.3))
                    # new_search = [i.split(' ', 1)[0] for i in new_search]

                    context = {"new_search": new_search}
                    return render(
                        request,
                        "association/search_results.html",
                        context,
                    )

                    # for search in new_search:
                    #     q_objects.add(
                    #         Q(target_species__icontains=search), Q.OR)

                proteins = Association.objects.filter(q_objects)
                proteins = _sorted_nicely(proteins, sort_key="name")

            elif field_type == "target order":
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(target_order__icontains=search), Q.OR)

                proteins = Association.objects.filter(q_objects)
                proteins = _sorted_nicely(proteins, sort_key="name")

                if not proteins:
                    words_target_order = list(
                        set(Association.objects.values_list("target_order", flat=True)))
                    new_search = []

                    for search in searches:
                        new_search.append(get_close_matches(
                            search, words_target_order, 1, 0.3))

                    context = {"new_search": new_search}
                    return render(
                        request,
                        "association/search_results.html",
                        context,
                    )

        return render(
            request,
            "association/search_results.html",
            {"proteins": proteins, "searches": searches},
        )
    return HttpResponseRedirect("/search_association/")


def keyword_confirm(request, name=None):
    """."""
    q_objects = Q()
    q_objects.add(Q(target_species__icontains=name), Q.OR)
    confirm_proteins = Association.objects.filter(q_objects)
    confirm_proteins = _sorted_nicely(confirm_proteins, sort_key="name")

    return render(
        request,
        "association/search_results.html",
        {"confirm_proteins": confirm_proteins},
    )


def home(request):
    # use 127.0.0.1:8000/api
    response = requests.get("http://ip-api.com/json/128.227.118.11")
    geodata = response.json()
    return render(request, "association/home_api.html", {"ip": geodata})


def heatmap_activity(request):
    return render(request, "association/heatmap_activity.html")

"""Pesticidal Protein Database related view functions."""


import re
import json
import textwrap
from io import StringIO
from Bio import SeqIO
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from database.admin import OldnameNewnameTableLeftResource, OldnameNewnameTableRightResource
from django.http import HttpResponse, HttpResponseRedirect
from database.models import PesticidalProteinDatabase, UserUploadData, Description, ProteinDetail, PesticidalProteinPrivateDatabase, StructureDatabase, OldnameNewnameTableLeft, OldnameNewnameTableRight
from database.forms import SearchForm, DownloadForm, ThreedomainDownloadForm, HolotypeForm
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Category20c, Spectral6, Category20
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource
from bokeh.transform import cumsum
from bokeh.embed import components
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from clustalanalysis.forms import AnalysisForm, UserDataForm
import pandas as pd
from numpy import pi
import xlwt
from database.filter_results import Search, filter_one_name, filter_one_oldname
from io import BytesIO
from itertools import chain
from rich.console import Console

console = Console()


def homepage(request):
    # return render(request, 'database/about_page.html')
    return render(request, 'index.html')


def about_protein(request, category=None):
    """Categorize the protein database with unqiue and first three letter pattern. Filters the protein based on these categories from public database as well as from private database

    Args:
        category: First three letter structural class

    Returns:
        Filtered list of proteins and their three letter descriptions

    """

    protein = PesticidalProteinDatabase.objects.filter(
        name__istartswith=category)
    private = PesticidalProteinPrivateDatabase.objects.filter(
        name__istartswith=category)

    protein_list = list(protein) + list(private)

    proteins = _sorted_nicely(protein_list, sort_key='name')
    # private = _sorted_nicely(private, sort_key='name')

    context = \
        {'proteins': proteins,
         'descriptions': Description.objects.filter(
             name__istartswith=category).order_by('name')
         }
    return render(request, 'list_protein.html', context)


def about_page(request):
    return render(request, 'database/about_page.html')


def statistics(request):
    """
    Return the number of categories in the database
    and its corresponding count.
    Holotype is a protein name ends in 1. Example: Cry1Aa1
    A holotype is a single protein name used to name the lower rank based on identity. Cry1Aa2 is named based on the identity to Cry1Aa1
    """
    category_count = {}
    category_holotype_count = {}
    category_prefixes = []
    total_holotype = 0

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name', flat=True).distinct()

    for category in categories:
        cat = category[:3]
        if category[-1] == '1' and not category[-2].isdigit():
            total_holotype += 1
            count = category_holotype_count.get(cat, 0)
            count += 1
            category_holotype_count[cat] = count

    category_count['Holotype'] = [total_holotype] * 2

    for category in categories:
        prefix = category[0:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    for category in category_prefixes:
        count = PesticidalProteinDatabase.objects.filter(
            name__istartswith=category).count()
        category_count[category] = [
            count, category_holotype_count.get(category, 0)]

    prefix_count_dictionary = {}
    for prefix in category_prefixes:
        prefix_count_dictionary[prefix] = category_count[prefix][0]

    prefix_count_dictionary.pop('Holotype', None)

    # data = pd.Series(prefix_count_dictionary).reset_index(
    #     name='value').rename(columns={'index': 'category'})
    # data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    # data['color'] = Category20c[len(prefix_count_dictionary)]
    #
    # p = figure(plot_height=600, plot_width=800, title="Pie Chart", toolbar_location=None,
    #            tools="hover", tooltips="@category: @value")
    #
    # p.wedge(x=0, y=1, radius=0.4,
    #         start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
    #         line_color="royalblue", fill_color='color', legend_group='category', source=data)
    #
    # script, div = components(p)

    context = \
        {'category_prefixes': category_prefixes,
         'category_count': category_count}

    return render(request, 'database/statistics.html', context)


def _sorted_nicely(l, sort_key=None):
    """
    Sort the given iterable in the way that humans expect.
    https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    """

    def convert(text): return int(text) if text.isdigit() else text
    if sort_key is None:
        def alphanum_key(key): return [convert(c)
                                       for c in re.split('([0-9]+)', key)]
    else:
        def alphanum_key(key): return [convert(c) for c in re.split(
            '([0-9]+)', getattr(key, sort_key))]
    return sorted(l, key=alphanum_key)


def categorize_database(request, category=None):
    """Categorize the protein database with unqiue and first three letter pattern. Filters the protein based on these categories from public database as well as from private database

    Args:
        category: First three letter structural class

    Returns:
        Filtered list of proteins and their three letter descriptions

    """

    protein = PesticidalProteinDatabase.objects.filter(
        name__istartswith=category)
    private = PesticidalProteinPrivateDatabase.objects.filter(
        name__istartswith=category)

    protein_list = list(protein) + list(private)

    proteins = _sorted_nicely(protein_list, sort_key='name')
    # private = _sorted_nicely(private, sort_key='name')

    context = \
        {'proteins': proteins,
         'descriptions': Description.objects.filter(
             name__istartswith=category).order_by('name')
         }
    return render(request, 'database/category_display_update.html', context)


def database(request):
    """
    The idea here is to list the categories along with the checkboxes.
    The user can select the desired category and click the download button.

    Returns:
        First three letter of the structural class
        Descriptions of the three letter structural class
        Three download forms
        See more details from the database.forms.py
    """

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name').distinct()
    category_prefixes = []
    for category in categories:
        prefix = category[0][:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    form1 = DownloadForm()
    form2 = ThreedomainDownloadForm()
    form3 = HolotypeForm()

    context = \
        {'category_prefixes': category_prefixes,
         'descriptions': Description.objects.all(),
         'form1': form1,
         'form2': form2,
         'form3': form3, }
    return render(request, 'database/database.html', context)


def search_database_home(request):
    """
    Search form: Search database by protein name
    User can search based on Name, Old Name, Accession, Holotype and Structure

    Returns:
        Search form
        See database.forms.py
    """
    form = SearchForm()
    return render(request, 'database/search_page.html', {'form': form})


def search_database(request):
    """
    Returns the results based on the search query. One complexity with the search here eg. Protein name are Cry1Aa1. It contains numeric, uppercase, lowercase.

    User can able to use keywords i.e.
    'Cry10*' - wildcard search should work
    Use multiple keywords with any separator (, or ;)
    Cry - should list all cry category
    Cry1 - should not return Cry10. Only Cry1's.
    Cry10 - should not return Cry1. Only Cry10's
    Cry10A
    Cry10Aa
    Cry10Aa1

    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        proteins = []
        single_digit = False
        if form.is_valid():
            query = form.cleaned_data['search_term']
            field_type = form.cleaned_data['search_fields']

            #searches = re.split(r':|, ?|\s |_ |. |; |\n', query)
            searches = re.split(r':|, ?|\s* |\n|;', query)

            if field_type == 'name':
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
                        q_search.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_double_digit():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_triple_digit():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_three_letter():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_three_letter_case():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    else:
                        q_objects.add(
                            Q(name__iexact=search), Q.OR)
                proteins1 = PesticidalProteinDatabase.objects.none()
                proteins2 = PesticidalProteinDatabase.objects.none()
                if q_objects:
                    proteins1 = PesticidalProteinDatabase.objects.filter(
                        q_objects)
                if q_search:
                    proteins2 = PesticidalProteinDatabase.objects.filter(
                        q_search)
                if proteins1 and proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = list(proteins1) + proteins2
                    proteins = _sorted_nicely(proteins, sort_key='name')
                elif proteins1:
                    proteins = _sorted_nicely(proteins1, sort_key='name')
                elif proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = _sorted_nicely(proteins2, sort_key='name')

            elif field_type == 'old name/other name':
                q_objects = Q()
                q_search = Q()
                for search in searches:
                    if Search(search).is_wildcard():
                        search = search[:-1]
                    else:
                        search = search
                    k = Search(search)
                    if k.is_fullname():
                        q_objects.add(Q(oldname__iexact=search), Q.OR)
                        q_objects.add(Q(othernames__iexact=search), Q.OR)
                    if k.fulltext():
                        q_objects.add(
                            Q(othernames__icontains=search), Q.OR)
                    if k.is_uppercase():
                        q_objects.add(Q(oldname__icontains=search), Q.OR)
                    if k.is_lowercase():
                        q_objects.add(Q(oldname__icontains=search), Q.OR)
                    if k.is_single_digit():
                        single_digit = True
                        q_search.add(
                            Q(oldname__icontains=search), Q.OR)
                    if k.is_double_digit():
                        q_objects.add(
                            Q(oldname__icontains=search), Q.OR)
                    if k.is_triple_digit():
                        q_objects.add(
                            Q(oldname__icontains=search), Q.OR)
                    if k.is_three_letter():
                        q_objects.add(
                            Q(oldname__icontains=search), Q.OR)
                    if k.is_three_letter_case():
                        q_objects.add(
                            Q(oldname__icontains=search), Q.OR)
                    if k.bthur0001_55730():
                        q_objects.add(
                            Q(othernames__iexact=search), Q.OR)
                    else:
                        q_objects.add(
                            Q(othernames__icontains=search), Q.OR)
                        q_objects.add(
                            Q(oldname__iexact=search), Q.OR)

                proteins1 = PesticidalProteinDatabase.objects.none()
                proteins2 = PesticidalProteinDatabase.objects.none()
                if q_objects:
                    proteins1 = PesticidalProteinDatabase.objects.filter(
                        q_objects)
                if q_search:
                    proteins2 = PesticidalProteinDatabase.objects.filter(
                        q_search)
                if proteins1 and proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = list(proteins1) + proteins2
                    proteins = _sorted_nicely(proteins, sort_key='name')
                elif proteins1:
                    proteins = _sorted_nicely(proteins1, sort_key='name')
                elif proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = _sorted_nicely(proteins2, sort_key='name')

            elif field_type == 'accession':
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(accession__icontains=search), Q.OR)

                proteins = PesticidalProteinDatabase.objects.filter(q_objects)
                proteins = _sorted_nicely(proteins, sort_key='name')
            elif field_type == 'holotype':
                # categories = \
                #     PesticidalProteinDatabase.objects.order_by(
                #         'name').values_list('name', flat=True).distinct()
                q_objects = Q()
                filtered_q_objects = Q()
                for search in searches:
                    q_objects.add(Q(name__icontains=search), Q.OR)

                categories = PesticidalProteinDatabase.objects.filter(
                    q_objects)

                for category in categories:
                    if category.name[-1] == '1' and not category.name[-2].isdigit():
                        filtered_q_objects.add(
                            Q(name__iexact=category.name), Q.OR)
                proteins = PesticidalProteinDatabase.objects.filter(
                    filtered_q_objects)
                proteins = _sorted_nicely(proteins, sort_key='name')

            elif field_type == 'structure':
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
                        q_search.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_double_digit():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_triple_digit():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_three_letter():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    if k.is_three_letter_case():
                        q_objects.add(
                            Q(name__icontains=search), Q.OR)
                    else:
                        q_objects.add(
                            Q(name__iexact=search), Q.OR)
                proteins1 = StructureDatabase.objects.none()
                proteins2 = StructureDatabase.objects.none()
                if q_objects:
                    proteins1 = StructureDatabase.objects.filter(
                        q_objects)
                if q_search:
                    proteins2 = StructureDatabase.objects.filter(
                        q_search)
                if proteins1 and proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = list(proteins1) + proteins2
                    proteins = _sorted_nicely(proteins, sort_key='name')
                elif proteins1:
                    proteins = _sorted_nicely(proteins1, sort_key='name')
                elif proteins2:
                    filtered_protein = filter_one_name(proteins2)
                    proteins2 = filtered_protein
                    proteins = _sorted_nicely(proteins2, sort_key='name')

                structures = _sorted_nicely(proteins, sort_key='name')
                return render(request, 'database/filter_structures.html', {'structures': structures})

        show_extra_data = False
        cry_count = 0
        for protein in proteins:
            if protein.name.startswith('Cry'):
                cry_count += 1
                protein.show_extra_data = True
        if cry_count == len(proteins):
            show_extra_data = True

        return render(request, 'database/search_results.html', {'proteins': proteins, 'show_extra_data': show_extra_data, 'searches': searches})
    return HttpResponseRedirect('/search_database_home/')


def add_cart(request):
    """
    Add the profiles to the cart.

    Search results provides list of proteins where user's have an option to select and add proteins to the cart. Add to cart uses 'request.session' to add the selected values.
    """

    if request.method == 'POST':

        selected_values = request.POST.getlist('name', [])
        previously_selected_values = request.session.get('list_names', [])
        previously_selected_values.extend(selected_values)
        request.session['list_names'] = previously_selected_values

        selected_nterminal = request.POST.getlist('nterminal', [])
        previously_selected_nterminal = request.session.get(
            'list_nterminal', [])
        previously_selected_nterminal.extend(selected_nterminal)
        request.session['list_nterminal'] = previously_selected_nterminal

        selected_middle = request.POST.getlist('middle', [])
        previously_selected_middle = request.session.get('list_middle', [])
        previously_selected_middle.extend(selected_middle)
        request.session['list_middle'] = previously_selected_middle

        selected_cterminal = request.POST.getlist('cterminal', [])
        previously_selected_cterminal = request.session.get(
            'list_cterminal', [])
        previously_selected_cterminal.extend(selected_cterminal)
        request.session['list_cterminal'] = previously_selected_cterminal

    return redirect("database")


def structures(request):
    """
    List of proteins that has solved structure in the protein data bank database
    """
    structures = \
        StructureDatabase.objects.order_by('name')

    context = \
        {'structures': structures}

    return render(request, 'database/structures.html', context)


def structure_pdbid(request, pdbid=None):
    """
    Categorize the protein database with unqiue, first three letter pattern.

        Args:
            pdbid: Protein Data Bank ID
            More information: https://www.rcsb.org/docs/general-help/identifiers-in-pdb

        Returns:
            - List of proteins in the structure database
            - Specific protein filtered through pdbid

        Note:
            This function is not used in the database.
    """

    protein = StructureDatabase.objects.filter(
        pdbid__istartswith=pdbid)
    structures = \
        StructureDatabase.objects.order_by('name')

    context = \
        {'proteins': protein,
         'structures': structures
         }
    return render(request, 'database/display_structure_pdbid.html', context)


def clear_session_database(request):
    """
    As the name suggest, it clears the selected proteins in the cart using database session.
    """

    session_key = list(request.session.keys())

    try:
        for key in session_key:
            del request.session[key]
    except:
        pass
    return redirect("view_cart")


def remove_cart(request, database_id):
    """
    Remove the selected proteins one by one from the cart.
    Assume you have selected proteins in search page and if you view the cart page, there is a table that shows selected prteins. These proteins can be removed from the cart using the trash-can/delete icon.

        Args:
            database_id:
    """

    protein = PesticidalProteinDatabase.objects.get(id=database_id)

    selected_values = request.session.get('list_names')
    nterminal = request.session.get('list_nterminal')
    middle = request.session.get('list_middle')
    cterminal = request.session.get('list_cterminal')

    try:
        selected_values.remove(protein.name)
    except:
        pass

    try:
        nterminal.remove(protein.name)
    except:
        pass

    try:
        middle.remove(protein.name)
    except:
        pass

    try:
        cterminal.remove(protein.name)
    except:
        pass

    request.session.modified = True

    # if selected_values:
    #     return redirect("view_cart")
    # message_profile = "Please add sequences to the cart"
    # messages.success(request, message_profile)
    return redirect("view_cart")


def cart_value(request):
    selected_values = request.session.get('list_names')
    nterminal = request.session.get('list_nterminal')
    middle = request.session.get('list_middle')
    cterminal = request.session.get('list_cterminal')
    values = []

    if nterminal:
        values += nterminal
    if middle:
        values += middle
    if cterminal:
        values += cterminal
    if selected_values:
        values += selected_values
    values = list(set(values))
    if values:
        number_of_proteins = len(values)
        return HttpResponse(json.dumps({'number_of_proteins': number_of_proteins}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'number_of_proteins': None}), content_type='application/json')


def view_cart(request):
    """
    View the selected proteins in the session and user uploaded sequences.
    """

    selected_values = request.session.get('list_names')
    selected_nterminal = request.session.get('list_nterminal')
    selected_middle = request.session.get('list_middle')
    selected_cterminal = request.session.get('list_cterminal')
    form_data = {
        'list_names': str(selected_values),
        'list_nterminal': str(selected_nterminal),
        'list_middle': str(selected_middle),
        'list_cterminal': str(selected_cterminal)
    }
    analysisform = AnalysisForm(form_data)
    userform = UserDataForm()
    analysisform.is_valid()
    values = []

    if selected_nterminal:
        values += selected_nterminal
    if selected_middle:
        values += selected_middle
    if selected_cterminal:
        values += selected_cterminal
    if selected_values:
        values += selected_values
    values = list(set(values))

    userdata = UserUploadData.objects.filter(
        session_key=request.session.session_key)

    if request.method == 'POST':
        userform = UserDataForm(request.POST, request.FILES,
                                session=request.session)

        if userform.is_valid():
            # print("form")
            messages.success(request, "file upload successful")

    context = {'proteins': PesticidalProteinDatabase.objects.all(),
               'selected_groups': values, 'userdata': userdata,
               'analysisform': analysisform, 'userform': userform}

    return render(request, 'database/search_user_data_update.html', context)


def clear_session_user_data(request):
    """Remove all the user uploaded proteins from the cart."""

    UserUploadData.objects.filter(
        session_key=request.session.session_key).delete()

    return redirect("view_cart")


def user_data_remove(request, id):
    """Remove the user uploaded proteins individually"""

    instance = UserUploadData.objects.get(
        session_key=request.session.session_key, id=id)
    instance.delete()

    return redirect("view_cart")


# def user_data(request):
#     """A user will upload the protein sequences in fasta format
#     and stored temporarily using the session."""
#
#     if request.method == 'POST':
#         file = request.POST['fulltextarea']
#         if not file:
#             message_profile = "Please add some sequences"
#             messages.success(request, message_profile)
#             return redirect("view_cart")
#
#         content = ContentFile(file)
#         content = filter(None, content)
#
#         for rec in SeqIO.parse(content, "fasta"):
#             name = rec.id
#             sequence = str(rec.seq)
#             UserUploadData.objects.create(
#                 session_key=request.session.session_key,
#                 name=name, sequence=sequence)
#         message_profile = "Added the user sequences"
#         messages.info(request, message_profile)
#
#     return redirect("view_cart")

def user_data(request):
    """A user will upload the protein sequences in fasta format
    and stored temporarily using the session."""

    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES,
                            session=request.session)

        if form.is_valid():
            # print("form")
            messages.success(request, "file upload successful")
        # print(form.errors)

    # return redirect("view_cart")
    return render(request, 'database/search_user_data_update.html', form)


@csrf_exempt
def download_sequences(request):
    """Download the selected and/or user uploaded protein sequences."""

    selected_values = request.session.get('list_names', [])
    list_nterminal = request.session.get('list_nterminal', [])
    list_middle = request.session.get('list_middle', [])
    list_cterminal = request.session.get('list_cterminal', [])

    values = []

    if list_nterminal:
        values += list_nterminal
    if list_middle:
        values += list_middle
    if list_cterminal:
        values += list_cterminal
    if selected_values:
        values += selected_values
    values = list(set(values))
    data = PesticidalProteinDatabase.objects.filter(name__in=values)

    userdata = UserUploadData.objects.filter(
        session_key=request.session.session_key)

    combined_selection = []

    if list_nterminal:
        combined_selection += list_nterminal
    if list_middle:
        combined_selection += list_middle
    if list_cterminal:
        combined_selection += list_cterminal
    if selected_values:
        combined_selection += selected_values

    accession = {}

    data = PesticidalProteinDatabase.objects.filter(
        name__in=combined_selection)
    if data:
        for item in data:
            accession[item.accession] = item

    protein_detail = ProteinDetail.objects.filter(
        accession__in=list(accession.keys()))

    file = StringIO()
    # buffer = BytesIO()
    for item in data:
        output = ''
        item_name = item.name
        # print("item_name", item_name)
        if item.name in list_nterminal:
            nterminal = [
                protein for protein in protein_detail if protein.accession == item.accession]
            item_name += '_d1'
            for item1 in nterminal:
                output += item1.get_endotoxin_n()
        if item.name in list_middle:
            middle = [
                protein for protein in protein_detail if protein.accession == item.accession]
            item_name += '_d2'
            for item1 in middle:
                output += item1.get_endotoxin_m()
        if item.name in list_cterminal:
            cterminal = [
                protein for protein in protein_detail if protein.accession == item.accession]
            # print(cterminal)
            item_name += '_d3'
            for item1 in cterminal:
                output += item1.get_endotoxin_c()
                # print("download output", output)
        if item.name in selected_values:
            fasta = textwrap.fill(item.sequence, 80)
            output += fasta
            # print(str_to_write)
            # file.write(str_to_write)

        if output:
            str_to_write = f">{item_name}\n{output}\n"
            file.write(str_to_write)

    for item in userdata:
        fasta = textwrap.fill(item.sequence, 80)
        if len(item.name) > 10:
            item.name = item.name[:10]
        str_to_write = f">{item.name}\n{fasta}\n"
        file.write(str_to_write)

    response = HttpResponse(file.getvalue(), content_type="text/plain")
    download_file = "cart_fasta_sequences.txt"
    response['Content-Disposition'] = 'attachment;filename=' + download_file
    response['Content-Length'] = file.tell()
    return response


def download_data(request):
    """List the categories for download."""

    categories = PesticidalProteinDatabase.objects.order_by(
        'name').values_list('name').distinct()

    category_prefixes = []
    for category in categories:
        prefix = category[0][:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    context = {
        'proteins': PesticidalProteinDatabase.objects.all(),
        'category_prefixes': category_prefixes,
        'descriptions': Description.objects.order_by('name')

    }
    return render(request, 'database/download_category.html', context)


def download_single_sequence(request, proteinname=None):
    """Download the fasta sequence by name."""

    protein = PesticidalProteinDatabase.objects.get(name=proteinname)
    file = StringIO()
    fasta = textwrap.fill(protein.sequence, 80)
    str_to_write = f">{protein.name}\n{fasta}\n"
    file.write(str_to_write)

    response = HttpResponse(file.getvalue(), content_type="text/plain")
    download_file = f"{proteinname}_fasta_sequence.txt"
    response['Content-Disposition'] = 'attachment;filename=' + download_file
    response['Content-Length'] = file.tell()
    return response


def download_category_form(request):

    form = DownloadForm()
    return render(request, 'database/download_form.html', form)


def download_category(request, category=None):
    """Download the fasta sequences for the category."""

    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            category = category.title()

            context = {
                'proteins': PesticidalProteinDatabase.objects.all(),
                'descriptions': Description.objects.order_by('name')

            }

            file = StringIO()
            data = list(context.get('proteins'))

            for item in data:
                if category in item.name:
                    fasta = textwrap.fill(item.sequence, 80)
                    str_to_write = f">{item.name}\n{fasta}\n"
                    file.write(str_to_write)
                else:
                    pass

            if 'All' in category:
                for item in data:
                    fasta = textwrap.fill(item.sequence, 80)
                    str_to_write = f">{item.name}\n{fasta}\n"
                    file.write(str_to_write)

            response = HttpResponse(file.getvalue(), content_type="text/plain")
            download_file = f"{category}_fasta_sequences.txt"
            response['Content-Disposition'] = 'attachment;filename=' + \
                download_file
            response['Content-Length'] = file.tell()
            return response
    form = DownloadForm()
    return render(request, 'database/download_form.html', form)


def category_form(request):
    form1 = DownloadForm()
    form2 = ThreedomainDownloadForm()
    form3 = HolotypeForm()

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
    }
    return render(request, 'database/download_form.html', context)


def category_download(request):
    if request.method == 'POST':
        categories = request.POST.getlist('category')
        print(categories)

        context = {
            'proteins': PesticidalProteinDatabase.objects.all()
        }

        file = StringIO()
        data = list(context.get('proteins'))

        for item in data:
            if 'All' in categories or item.name[:3].lower() in str(categories):
                fasta = textwrap.fill(item.sequence, 80)
                str_to_write = f">{item.name}\n{fasta}\n"
                file.write(str_to_write)

        # if :
        #     for item in data:
        #         fasta = textwrap.fill(item.sequence, 80)
        #         str_to_write = f">{item.name}\n{fasta}\n"
        #         file.write(str_to_write)

        response = HttpResponse(file.getvalue(), content_type="text/plain")
        download_file = f"{'_'.join(categories)}_fasta_sequences.txt"
        response['Content-Disposition'] = 'attachment;filename=' + download_file
        response['Content-Length'] = file.tell()
        return response


def threedomain_download(request):
    if request.method == 'POST':
        type_option = request.POST.getlist('threedomain')
        file = StringIO()

        accession = {}
        output = ''

        data = PesticidalProteinDatabase.objects.filter(
            name__istartswith="cry").order_by('name')
        if data:
            for item in data:
                # if item.name[-1] == '1' and not item.name[-2].isdigit():
                accession[item.accession] = item

        protein_detail = ProteinDetail.objects.filter(
            accession__in=list(accession.keys()))

        protein_data = PesticidalProteinDatabase.objects.filter(
            accession__in=list(accession.keys()))

        count = 0
        for item in protein_data:
            output = ''
            domain_name = ''
            if 'domain1' in type_option:
                nterminal = [
                    protein for protein in protein_detail if protein.accession == item.accession]
                for item1 in nterminal:
                    count += 1
                    output += item1.get_endotoxin_n()
                    domain_name += '_d1'
            if 'domain2' in type_option:
                nterminal = [
                    protein for protein in protein_detail if protein.accession == item.accession]
                for item1 in nterminal:
                    count += 1
                    output += item1.get_endotoxin_m()
                    domain_name += '_d2'
            if 'domain3' in type_option:
                nterminal = [
                    protein for protein in protein_detail if protein.accession == item.accession]
                for item1 in nterminal:
                    count += 1
                    output += item1.get_endotoxin_c()
                    domain_name += '_d3'
            if 'full_length' in type_option:
                nterminal = [
                    protein for protein in protein_detail if protein.accession == item.accession]
                for item1 in nterminal:
                    count += 1
                    output += item1.sequence
                    domain_name += '_full_length'
            if output:
                str_to_write = f">{item.name}{domain_name}\n{output}\n"
                file.write(str_to_write)

        response = HttpResponse(
            file.getvalue(), content_type="text/plain")
        download_file = f"{'_'.join(type_option)}_threedomain_fasta_sequences.txt"
        response['Content-Disposition'] = 'attachment;filename=' + \
            download_file
        response['Content-Length'] = file.tell()
        return response


def holotype_download(request):
    if request.method == 'POST':
        type_option = request.POST.getlist('holotype')
        file = StringIO()

        accession = {}
        output = ''

        data = PesticidalProteinDatabase.objects.filter(
            name__istartswith="cry").order_by('name').distinct()
        if data:
            for item in data:
                if item.name[-1] == '1' and not item.name[-2].isdigit():
                    str_to_write = f">{item.name}\n{item.sequence}\n"
                    file.write(str_to_write)

        response = HttpResponse(
            file.getvalue(), content_type="text/plain")
        download_file = f"{'_'.join(type_option)}_fasta_sequences.txt"
        response['Content-Disposition'] = 'attachment;filename=' + \
            download_file
        response['Content-Length'] = file.tell()
        return response


def protein_detail(request, name):

    data = PesticidalProteinDatabase.objects.filter(name=name).first()
    histo = data.get_sequence_count_aminoacids()

    keys, values = zip(*histo.items())
    language = list(keys)
    counts = list(values)

    p = figure(x_range=language, plot_height=1000, plot_width=1000,
               toolbar_location="below", tools="pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair")

    source = ColumnDataSource(
        data=dict(language=language, counts=counts, color=Category20[20]))
    p.add_tools(LassoSelectTool())
    p.add_tools(WheelZoomTool())

    p.vbar(x='language', top='counts', width=0.8, color='color',
           legend_group="language", source=source)
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.y_range.start = 0

    script, div = components(p)

    context = {'proteins': PesticidalProteinDatabase.objects.filter(name=name),
               'script': script, 'div': div
               }

    return render(request, 'database/protein_detail.html', context)


def old_name_new_name(request):
    table1 = OldnameNewnameTableLeft.objects.all()
    table2 = OldnameNewnameTableRight.objects.all()

    context = {'table1': table1,
               'table2': table2,
               }
    return render(request, 'database/old_name_new_name.html', context)


def export_new_name_table(request):
    left_resource = OldnameNewnameTableLeftResource()
    dataset_left = left_resource.export()
    response = HttpResponse(dataset_left.xlsx, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="organized_newname.xlsx"'
    return response


def export_old_name_table(request):
    right_resource = OldnameNewnameTableRightResource()
    dataset_right = right_resource.export()
    response = HttpResponse(dataset_right.xlsx, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="organized_oldname.xlsx"'
    return response

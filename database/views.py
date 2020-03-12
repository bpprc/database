"""Database related view functions."""


import re
import json
import textwrap
from io import StringIO
from Bio import SeqIO
from django.shortcuts import render, redirect, render_to_response
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from database.models import PesticidalProteinDatabase, UserUploadData, Description, ProteinDetail
from database.forms import FeedbackDataForm, SearchForm
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Category20c, Spectral6, Category20
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource
from bokeh.transform import cumsum
from bokeh.embed import components
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
from numpy import pi


def home(request):
    """Loads the homepage."""
    category_count = {}
    category_holotype_count = {}
    category_prefixes = []
    total_holotype = 0

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name', flat=True).distinct()  # why you need flat=True

    for category in categories:
        cat = category[:3]
        if category[-1] == '1' and not category[-2].isdigit():
            total_holotype += 1
            count = category_holotype_count.get(cat, 0)
            count += 1
            category_holotype_count[cat] = count

    category_count['Holotype'] = total_holotype

    for category in categories:
        prefix = category[0:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    for category in category_prefixes:
        count = PesticidalProteinDatabase.objects.filter(
            name__istartswith=category).count()
        category_count[category] = [
            count, category_holotype_count.get(category, 0)]

    context = \
        {'category_prefixes': category_prefixes,
         'category_count': category_count, }

    return render(request, 'database/home.html', context)


def about_page(request):
    return render(request, 'database/about_page.html')


def statistics(request):
    """Loads the homepage."""
    category_count = {}
    category_holotype_count = {}
    category_prefixes = []
    total_holotype = 0

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name', flat=True).distinct()  # why you need flat=True

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

    # print(category_prefixes)
    # print(category_count)
    # print(type(category_prefixes))
    # print(type(category_count))
    prefix_count_dictionary = {}
    for prefix in category_prefixes:
        prefix_count_dictionary[prefix] = category_count[prefix][0]

    # prefix_count_dictionary = dict(zip(category_prefixes, category_count))
    # print(prefix_count_dictionary)
    prefix_count_dictionary.pop('Holotype', None)

    data = pd.Series(prefix_count_dictionary).reset_index(
        name='value').rename(columns={'index': 'category'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(prefix_count_dictionary)]

    p = figure(plot_height=600, plot_width=800, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@category: @value")

    # p.wedge(x=0, y=1, radius=0.4,
    #         start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
    #         line_color="royalblue", fill_color='color', legend_group='category', source=data)

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="royalblue", fill_color='color', legend_group='category', source=data)

    script, div = components(p)

    context = \
        {'category_prefixes': category_prefixes,
         'category_count': category_count,
         'script': script, 'div': div}

    return render(request, 'database/statistics.html', context)


def privacy_policy(request):
    return render(request, 'database/privacy-policy.html', context)


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


def categorize_database(request, category=None):
    """Categorize the protein database with unqiue, first three letter pattern."""

    proteins = PesticidalProteinDatabase.objects.filter(
        name__istartswith=category)
    proteins = _sorted_nicely(proteins, sort_key='name')
    context = \
        {'proteins': proteins,
         'descriptions': Description.objects.filter(
             name__istartswith=category).order_by('name')
         }
    return render(request, 'database/category_display_update.html', context)


def database(request):
    """Returns the protein list for the categories from the database."""

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name').distinct()
    category_prefixes = []
    for category in categories:
        prefix = category[0][:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    context = \
        {'category_prefixes': category_prefixes,
         'descriptions': Description.objects.all()}
    return render(request, 'database/database.html', context)

    # if request.method == 'POST':
    #     form = SearchForm(search_term=request.POST)
    #
    #     if search_form.is_valid():
    #         search_term = form.cleaned_data['search_term']

# def search_database_home(request):
#     form = SearchForm()
#     return render(request, 'database/search_page_update.html', {'form': form})
#
# def search_database(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             keyword = form.cleaned_data['search_term']
#             print(keyword)
#
#             return render(request, 'database/search_page_update.html', form)
#
#     return HttpResponseRedirect('/search_database_home/')


def search_database_home(request):
    form = SearchForm()
    return render(request, 'database/search_page.html', {'form': form})


def search_database(request):
    """Returns the results based on the search query."""
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            query = form.cleaned_data['search_term']
            field_type = form.cleaned_data['search_fields']

            searches = re.split(r':|, ?|\s |\- |_ |. |; |\*|\n',
                                query)

            if field_type == 'name':
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(name__icontains=search), Q.OR)

                proteins = PesticidalProteinDatabase.objects.filter(q_objects)
            elif field_type == 'oldname':
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(oldname__icontains=search), Q.OR)

                proteins = PesticidalProteinDatabase.objects.filter(q_objects)

            elif field_type == 'accession':
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(accession__icontains=search), Q.OR)

                proteins = PesticidalProteinDatabase.objects.filter(q_objects)

            elif field_type == 'year':
                q_objects = Q()
                for search in searches:
                    q_objects.add(Q(year__icontains=search), Q.OR)

                proteins = PesticidalProteinDatabase.objects.filter(q_objects)

            return render(request, 'database/search_results.html', {'proteins': proteins})
    return HttpResponseRedirect('/search_database_home/')


def add_cart(request):
    """Add the profiles to the cart."""

    if request.method == 'POST':
        selected_values = request.POST.getlist('name', [])
        previously_selected_values = request.session.get('list_names', [])
        previously_selected_values.extend(selected_values)

        request.session['list_names'] = previously_selected_values
        profile_length = len(selected_values)
        message_profile = \
            "Selected {} proteins added to the cart".format(profile_length)
        messages.success(request, message_profile)

    return redirect("search_database")


def clear_session_database(request):
    """Clear the database session."""

    session_key = list(request.session.keys())

    for key in session_key:
        del request.session[key]
    return redirect("view_cart")


def remove_cart(request, database_id):
    """Remove the selected proteins one by one from the cart."""

    protein = PesticidalProteinDatabase.objects.get(id=database_id)

    selected_values = request.session.get('list_names')
    selected_values.remove(protein.name)
    request.session.modified = True

    if selected_values:
        return redirect("view_cart")
    message_profile = "Please add sequences to the cart"
    messages.success(request, message_profile)
    return redirect("search_database")


def cart_value(request):
    selected_values = request.session.get('list_names')
    if selected_values:
        number_of_proteins = len(selected_values)
        return HttpResponse(json.dumps({'number_of_proteins': number_of_proteins}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'number_of_proteins': None}), content_type='application/json')


def view_cart(request):
    """View the selected proteins in the session and user uploaded sequences."""

    selected_values = request.session.get('list_names')

    userdata = \
        UserUploadData.objects.filter(session_key=request.session.session_key)

    context = {'proteins': PesticidalProteinDatabase.objects.all(),
               'selected_groups': selected_values, 'userdata': userdata}
    if selected_values:
        profile_length = len(selected_values)
        message_profile = "Selected {} proteins added to the cart".format(
            profile_length)
        messages.success(request, message_profile)
    else:
        message_profile = "Please add sequences to the cart"
        messages.success(request, message_profile)

    return render(request, 'database/search_user_data.html', context)


def clear_session_user_data(request):
    """Remove all the user uploaded proteins from the cart."""

    UserUploadData.objects.filter(
        session_key=request.session.session_key).delete()

    return redirect("view_cart")


def user_data_remove(request, id):
    """Remove the user uploaded proteins individually"""

    # delte older temp files
    # _delete_temp_files(path=TEMP_DIR, days=TEMP_LIFE)

    instance = \
        UserUploadData.objects.get(session_key=request.session.session_key,
                                   id=id)
    instance.delete()

    return redirect("view_cart")


def user_data(request):
    """A user will upload the protein sequences in fasta format
    and stored temporarily using the session."""

    if request.method == 'POST':
        file = request.POST['fulltextarea']
        if not file:
            message_profile = "Please add some sequences"
            messages.success(request, message_profile)
            return redirect("view_cart")

        content = ContentFile(file)
        content = filter(None, content)

        for rec in SeqIO.parse(content, "fasta"):
            name = rec.id
            sequence = str(rec.seq)
            UserUploadData.objects.create(
                session_key=request.session.session_key,
                name=name, fastasequence=sequence)
        message_profile = "Added the user sequences"
        messages.info(request, message_profile)

    return redirect("view_cart")


@csrf_exempt
def download_sequences(request):
    """Download the selected and/or user uploaded protein sequences."""

    selected_values = request.session.get('list_names', [])
    userdata = \
        UserUploadData.objects.filter(session_key=request.session.session_key)

    if not selected_values and not userdata.exists():
        message_profile = "Please add sequences to the cart"
        messages.success(request, message_profile)
        return redirect("view_cart")

    file = StringIO()
    data = \
        PesticidalProteinDatabase.objects.filter(name__in=selected_values)
    for item in data:
        fasta = textwrap.fill(item.sequence, 80)
        str_to_write = f">{item.name}\n{fasta}\n"
        file.write(str_to_write)

    for record in userdata:
        fasta = textwrap.fill(record.sequence, 80)
        str_to_write = f">{record.name}\n{fasta}\n"
        file.write(str_to_write)

    response = HttpResponse(file.getvalue(), content_type="text/plain")
    response['Content-Disposition'] = \
        'attachment;filename=data_fasta.txt'
    response['Content-Length'] = file.tell()
    return response


def download_data(request):
    """List the categories for download."""

    categories = \
        PesticidalProteinDatabase.objects.order_by(
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
    download_file = f"{proteinname}_fasta_sequences.txt"
    response['Content-Disposition'] = 'attachment;filename=' + download_file
    response['Content-Length'] = file.tell()
    return response


def download_category(request, category=None):
    """Download the fasta sequences for the category."""

    context = {
        'proteins': PesticidalProteinDatabase.objects.all()
    }
    category = category.title()
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
    response['Content-Disposition'] = 'attachment;filename=' + download_file
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


def emailView(request):
    if request.method == 'GET':
        form = FeedbackDataForm()
    else:
        form = FeedbackDataForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "database/feedback.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')


def page_not_found(request, exception):
    """ Return 404 error page."""

    return render(request, 'database/404.html', status=404)


def server_error(request):
    """ Return server error."""

    return render(request, 'database/500.html', status=500)


def faq(request):
    return render(request, 'database/faq.html')

# def _delete_temp_files(path=TEMP_DIR, days=TEMP_LIFE):
#     """
#     Delete older temp files based on TEMP_DIR and TEMP_LIFE.
#     Please change the number of days in the BPPRC.settings files
#     """
#     import time
#
#     current_time = time.time()
#
#     for file in os.listdir(path):
#         file = os.path.join(path, file)
#         if os.stat(file).st_mtime < current_time - days * 86400:
#             os.remove(file)


def _get_current_date():

    import datetime

    now = datetime.datetime.now()

    return str(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))

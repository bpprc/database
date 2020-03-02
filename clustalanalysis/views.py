from django.shortcuts import render, redirect
from database.models import PesticidalProteinDatabase, UserUploadData, ProteinDetail
from clustalanalysis.forms import AnalysisForm, DendogramForm
from django import forms
from subprocess import Popen, PIPE
from ete3 import Tree, TreeStyle, faces
from Bio.Align.Applications import ClustalOmegaCommandline
from django.http import HttpResponseRedirect
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from django.contrib import messages
from clustalanalysis.forms import AnalysisForm
from Bio import AlignIO
import tempfile
import textwrap
import os
from database.models import PesticidalProteinDatabase, UserUploadData, Description, ProteinDetail
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Category20c, Spectral6, Category20
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource
from bokeh.transform import cumsum
from bokeh.embed import components
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
from numpy import pi



def domain_analysis_homepage(request):
    """This loads the bestmatchfinder homepage."""
    form = AnalysisForm()
    return render(request, 'clustalanalysis/domain_cry.html', {'form': form})

def domain_anlaysis(request):
    form = AnalysisForm()
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['session_list_names'] = request.session.get('list_names', [])
        form = AnalysisForm(post_values)
        if form.is_valid():
            domain_type = form.cleaned_data.get('domain_type')
            rooted_tree = form.save()
            # rooted_tree = "tree"

            context = {
                'tree' : rooted_tree
            }
            return render(request, 'clustalanalysis/domain_cry_tree.html', context)
        print(form.errors)
        context = {'form': form}
        return render(request, 'clustalanalysis/domain_cry.html', context)

    return HttpResponseRedirect('/domain_analysis_homepage/')


def dendogram_homepage(request):
    """This loads the bestmatchfinder homepage."""
    form = DendogramForm()
    return render(request, 'clustalanalysis/dendogram_homepage.html', {'form': form})


def dendogram(request):
    form = DendogramForm()
    if request.method == 'POST':
        form = DendogramForm(request.POST)
        if form.is_valid():
            # category_type = form.cleaned_data.get('category_type')
            # print(category_type)
            rooted_tree = form.save()
            # rooted_tree = "tree"

            context = {
                'tree' : rooted_tree,
            }
            return render(request, 'clustalanalysis/dendogram.html', context)

        context = {'form': form}
        return render(request, 'clustalanalysis/dendogram.html', context)

    return HttpResponseRedirect('/dendogram_homepage/')



def protein_analysis(request):

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name', flat=True).distinct() #why you need flat=True

    category_prefixes = []
    for category in categories:
        prefix = category[:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    dict_fasta_category = {}
    dict_histo_category = {}
    for category in category_prefixes:
        fasta = ''
        k = PesticidalProteinDatabase.objects.filter(name__istartswith=category)
        for s in k:
            fasta += s.fastasequence
        dict_fasta_category[category] = fasta


    for key,value in dict_fasta_category.items():
        x = ProteinAnalysis(value)
        k = x.get_amino_acids_percent()
        dict_m = {}
        for i in k:
            dict_m[i] = round(k[i], 2)
        dict_histo_category[key] = dict_m

    keys, values = zip(*dict_histo_category.items())

    language = list(keys)
    counts = list(values)

    for f,b in zip(language, counts):
        print(type(f))


    p = figure(x_range=language, plot_height=1000, plot_width=1000,
               toolbar_location="below", tools="pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair")

    source = ColumnDataSource(data=dict(language=language, counts=counts, color=Category20[20]))
    p.add_tools(LassoSelectTool())
    p.add_tools(WheelZoomTool())

    p.vbar(x='language', top='counts', width=0.8, color='color', legend_group="language", source=source)
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.y_range.start = 0

    script, div = components(p)

    context = {
               'script': script, 'div':div }

    return render(request, 'clustalanalysis/protein_analysis.html', context)

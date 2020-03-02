# Author: Suresh Pannerselvam
# License: GPL v3
# Copyright @ 2019 Suresh Pannerselvam

"""This loads the bestmatchfinder homepage."""

import os
import tempfile
import textwrap
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from database.models import PesticidalProteinDatabase
from bestmatchfinder.forms import SearchDatabaseForm, SequenceForm
from bestmatchfinder import submit_single_sequence, submit_two_sequences



def bestmatchfinder_home(request):
    """This loads the bestmatchfinder homepage."""
    form = SequenceForm()
    return render(request, 'bestmatchfinder/best_match_finder.html', {'form': form})


def run_needle_server(request):
    """This loads the bestmatchfinder homepage."""
    if request.method == 'POST':
        form = SequenceForm(request.POST)
        if form.is_valid():
            protein = form.cleaned_data['sequence_in_form']
            align = submit_single_sequence.align.run_bug(protein)

            context = {
                'align': align
            }
            return render(request, 'bestmatchfinder/needle.html', context)
        return render(request, 'bestmatchfinder/best_match_finder.html', {'form': form})
    return HttpResponseRedirect('/bestmatchfinder_home/')


def bestmatchfinder_database(request):
    """This loads the bestmatchfinder homepage."""
    form = SearchDatabaseForm()
    return render(request, 'bestmatchfinder/best_match_finder_database.html', {'form': form})

def bestmatchfinder_database_sequence_run(request):
    """ This runs bestmatchfinder from the database."""
    if request.method == 'POST':
        form = SearchDatabaseForm(request.POST)
        if form.is_valid():
            protein1 = form.cleaned_data['protein_id1']
            protein2 = form.cleaned_data['protein_id2']
            tool = form.cleaned_data['tool']

            if protein1:
                protein1 = os.path.join(settings.MEDIA_ROOT, protein1.fastasequence_file.path)
            else:
                protein1 = form.cleaned_data['sequence1_in_form']

            if protein2:
                protein2 = os.path.join(settings.MEDIA_ROOT, protein2.fastasequence_file.path)
            else:
                protein2 = form.cleaned_data['sequence2_in_form']

            align = submit_two_sequences.needle.needle_alignment(protein1, protein2)

            context = {
                'align': align
            }

            return render(request, 'bestmatchfinder/needle1.html', context)
        return render(request, 'bestmatchfinder/best_match_finder_database.html', {'form': form})
    return HttpResponseRedirect('/bestmatchfinder_database/')

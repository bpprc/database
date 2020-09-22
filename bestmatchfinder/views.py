# Author: Suresh Pannerselvam
# License: GPL v3
# Copyright @ 2019 Suresh Pannerselvam

"""This loads the bestmatchfinder homepage."""

import os
import tempfile
import textwrap
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from database.models import PesticidalProteinDatabase
from bestmatchfinder.forms import SearchDatabaseForm, SequenceForm
from bestmatchfinder import submit_single_sequence, submit_two_sequences
from BPPRC.settings import TEMP_DIR, TEMP_LIFE

from celery import current_app
from .tasks import run_needle


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


def run_needle_server_celery(request):
    """This loads the bestmatchfinder homepage."""
    if request.method == 'POST':
        form = SequenceForm(request.POST)
        if form.is_valid():
            context = {}
            protein = form.cleaned_data['sequence_in_form']
            # align = submit_single_sequence.align.run_bug(protein)
            # print('protein file name', protein)

            task = run_needle.delay(protein)
            # print('view task result', task)

            context['task_id'] = task.id
            context['task_status'] = task.status
            context['task'] = task.info

            return render(request, 'bestmatchfinder/needle_processing.html', context)

        return render(request, 'bestmatchfinder/best_match_finder.html', {'form': form})
    return HttpResponseRedirect('/bestmatchfinder_home/')


def taskstatus_needle_celery(request, task_id):

    if request.method == 'GET':
        print("entering the function taskstatus")
        task = current_app.AsyncResult(task_id)
        print("taskStatus", task)
        context = {'task_status': task.status,
                   'task_id': task.id, 'task': task}

        if task.status == 'SUCCESS':
            context['align'] = task.get()
            print(context)
            return render(request, 'bestmatchfinder/needle.html', context)

        elif task.status == 'PENDING':
            context['results'] = task
            return render(request, 'bestmatchfinder/needle_processing.html', context)

        context['error'] = task
        return render(request, 'bestmatchfinder/needle_processing.html', context)


def celery_task_status(request, task_id):

    print("entering the function taskstatus")
    task = current_app.AsyncResult(task_id)
    print("taskStatus", task)
    context = {'task_status': task.status,
               'task_id': task.id}
    return JsonResponse(context)


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
            data = form.cleaned_data
            name1 = data['protein_id1'] or data['sequence1_in_form']
            name2 = data['protein_id2'] or data['sequence2_in_form']

            try:
                query = "Query: " + name1.name + ' '
                subject = "Subject: " + name2.name + ' '
                tool = form.cleaned_data['tool']
            except:
                query = "Query: " + name1 + ' '
                subject = "Subject: " + name2 + ' '
                tool = form.cleaned_data['tool']

            if protein1:
                protein1 = os.path.join(
                    settings.MEDIA_ROOT, protein1.fastasequence_file.path)
            else:
                protein1 = form.cleaned_data['sequence1_in_form']

            if protein2:
                protein2 = os.path.join(
                    settings.MEDIA_ROOT, protein2.fastasequence_file.path)
            else:
                protein2 = form.cleaned_data['sequence2_in_form']

            if tool == 'needle':
                align = submit_two_sequences.needle.needle_alignment(
                    protein1, protein2)
            else:
                align = submit_two_sequences.needle.blast_alignment(
                    protein1, protein2)
                removed_blast_title = align.split('>')[1]
                removed_blast_title = removed_blast_title.lstrip()
                filtered_result = removed_blast_title.split('Lambda')
                align = query + subject + '\n\n' + filtered_result[0]

            context = {
                'align': align
            }

            return render(request, 'bestmatchfinder/needle1.html', context)
        return render(request, 'bestmatchfinder/best_match_finder_database.html', {'form': form})
    return HttpResponseRedirect('/bestmatchfinder_database/')

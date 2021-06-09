# Author: Suresh Pannerselvam
# License: GPL v3
# Copyright @ 2019 Suresh Pannerselvam

"""This loads the bestmatchfinder homepage."""

import os

from celery import current_app
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from bestmatchfinder import submit_single_sequence, submit_two_sequences
from bestmatchfinder.forms import SearchDatabaseForm, SequenceForm

from .tasks import run_needle


def bestmatchfinder_home(request):
    """This loads the bestmatchfinder homepage."""

    form = SequenceForm()
    return render(request, "newwebpage/best_match_finder.html", {"form": form})


def run_needle_server(request):
    """This loads the bestmatchfinder homepage."""
    if request.method == "POST":
        form = SequenceForm(request.POST)
        if form.is_valid():
            protein = form.cleaned_data["sequence_in_form"]
            align = submit_single_sequence.align.run_bug(protein)

            context = {"align": align}
            return render(request, "newwebpage/needle.html", context)
        return render(request, "newwebpage/best_match_finder.html", {"form": form})
    return HttpResponseRedirect("/bestmatchfinder_home/")


def run_needle_server_celery(request):
    """This loads the bestmatchfinder homepage."""
    if request.method == "POST":
        form = SequenceForm(request.POST)
        if form.is_valid():
            context = {}
            protein = form.cleaned_data["sequence_in_form"]
            # align = submit_single_sequence.align.run_bug(protein)
            # print('protein file name', protein)

            task = run_needle.delay(protein)
            # print('view task result', task)

            context["task_id"] = task.id
            context["task_status"] = task.status
            context["task"] = task.info

            return render(request, "newwebpage/needle_processing.html", context)

        return render(request, "newwebpage/best_match_finder.html", {"form": form})
    return HttpResponseRedirect("/bestmatchfinder_home/")


def taskstatus_needle_celery(request, task_id):

    if request.method == "GET":
        print("entering the function taskstatus")
        task = current_app.AsyncResult(task_id)
        print("taskStatus", task)
        context = {
            "task_status": task.status,
            "task_id": task.id,
            "task": task,
        }

        if task.status == "SUCCESS":
            context["align"] = task.get()
            print(context)
            return render(request, "newwebpage/needle.html", context)

        elif task.status == "PENDING":
            context["results"] = task
            return render(request, "newwebpage/needle_processing.html", context)

        context["error"] = task
        # print(task)
        return render(request, "newwebpage/needle_processing.html", context)


def celery_task_status(request, task_id):

    print("entering the function taskstatus")
    task = current_app.AsyncResult(task_id)
    print("taskStatus", task)
    context = {"task_status": task.status, "task_id": task.id}
    return JsonResponse(context)


def bestmatchfinder_database(request):
    """This loads the bestmatchfinder homepage."""
    form = SearchDatabaseForm()
    return render(
        request,
        "newwebpage/best_match_finder_database.html",
        {"form": form},
    )


def string_replace(string):
    path = os.path.join(settings.MEDIA_ROOT, "fastasequence_files/")
    empty = ''
    result = string.replace(path, empty)
    return result


def bestmatchfinder_database_sequence_run(request):
    """This runs bestmatchfinder from the database."""
    if request.method == "POST":
        form = SearchDatabaseForm(request.POST)

        if form.is_valid():
            protein1 = form.cleaned_data["protein_id1"]
            protein2 = form.cleaned_data["protein_id2"]
            # sequence1 = form.cleaned_data['sequence1_in_form']
            # sequence2 = form.cleaned_data['sequence2_in_form']
            tool = form.cleaned_data["tool"]
            # data = form.cleaned_data
            # name1 = data['protein_id1'] or data['sequence1_in_form']
            # name2 = data['protein_id2'] or data['sequence2_in_form']
            #
            # try:
            #     query = "Query: " + name1.name + ' '
            #     subject = "Subject: " + name2.name + ' '
            # except:
            #     query = "Query: " + name1 + ' '
            #     subject = "Subject: " + name2 + ' '

            if protein1:
                protein1 = os.path.join(
                    settings.MEDIA_ROOT,
                    protein1.fastasequence_file.path,
                )
            else:
                protein1 = form.cleaned_data["sequence1_in_form"]

            if protein2:
                protein2 = os.path.join(
                    settings.MEDIA_ROOT,
                    protein2.fastasequence_file.path,
                )
            else:
                protein2 = form.cleaned_data["sequence2_in_form"]

            if tool == "needle":
                align = submit_two_sequences.needle.needle_alignment(
                    protein1, protein2)
            else:
                align = submit_two_sequences.needle.blast_alignment(
                    protein1, protein2)
                removed_blast_title = align.split(">")[1]
                removed_blast_title = removed_blast_title.lstrip()
                filtered_result = removed_blast_title.split("Lambda")
                protein1 = string_replace(protein1)
                protein2 = string_replace(protein2)
                protein1 = "Protein1 : " + protein1 + "\n"
                protein2 = " Protein2 : " + protein2 + "\n"
                align = protein1 + protein2 + \
                    "\n\n" + filtered_result[0]

            context = {"align": align}

            return render(request, "newwebpage/two_sequence_needle.html", context)
        return render(
            request,
            "newwebpage/best_match_finder_database.html",
            {"form": form},
        )
    return HttpResponseRedirect("/bestmatchfinder_database/")

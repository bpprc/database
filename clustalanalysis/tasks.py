import os
from zipfile import ZipFile

from celery import shared_task
from PIL import Image

from django.conf import settings

from clustalanalysis import run_clustal


@shared_task
def create_tree(inputfile, outputfile):
    try:
        print("This is clustal function")
        result_file = run_clustal.run_clustal(inputfile, outputfile)
        return outputfile
    except IOError as e:
        return e

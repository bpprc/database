import textwrap
import itertools
import os
import re
import subprocess

from django.conf.urls.static import settings
from django.core.management.base import BaseCommand

# Import the model
from database.models import PesticidalProteinDatabase
from bestmatchfinder import submit_two_sequences

NEEDLE_PATH = os.environ.get("NEEDLE_PATH")


def _cmdline(command):
    """This loads the bestmatchfinder homepage."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    out, error = process.communicate()
    # print("out", out)
    # print("error", error)
    return out


def _run_needle(file1, file2):
    """This loads the bestmatchfinder homepage."""

    cmd = (
        NEEDLE_PATH
        + "needle -datafile EBLOSUM62 -auto Y"
        + " -asequence "
        + file1
        + " -bsequence "
        + file2
        + " -sprotein1 Y -sprotein2 Y "
        + " -auto -stdout"
    )
    results = _cmdline(cmd).decode("utf-8")
    identity = re.search(r"\d{1,3}\.\d*\%", results)
    if identity:
        identity = identity.group()
        identity = identity.replace("%", "")
        print(identity)
        return identity


class Command(BaseCommand):
    help = "Loads data from PesticidalProteinDatabase.csv"

    def handle(self, *args, **kwargs):

        file_path = settings.MEDIA_ROOT + "/bestmatch_two_sequences/"
        #categories = PesticidalProteinDatabase.objects.all()
        # for category in categories:
        #     fasta = textwrap.fill(category.sequence, 80)
        #     str_to_write = f">{category.name}\n{fasta}\n"
        #     filename = file_path + category.name
        #     with open(filename, 'w') as the_file:
        #         the_file.write(str_to_write)

        folder1 = os.listdir(file_path)
        folder2 = os.listdir(file_path)

        for file1, file2 in zip(folder1, folder2):
            file1path = file_path + file1
            file2path = file_path + file2
            align = submit_two_sequences.needle.needle_alignment(
                file1path, file2path)

            identity = re.search(r"\d{1,3}\.\d*\%", align)
            if identity:
                identity = identity.group()
                identity = identity.replace("%", "")
            try:
                if float(identity) == 100.0:
                    print(file1, file2)
                    # if file1 != file2:
                    #print(file1, file2)
            except:
                pass

        # Run blast with all the files
        # If it is 100% show the protein names in a model

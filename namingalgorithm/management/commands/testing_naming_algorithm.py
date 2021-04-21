from django.core.management.base import BaseCommand
from naming_package import run_data
from database.models import PesticidalProteinDatabase
from namingalgorithm.models import UserSubmission
from django.conf import settings
from pathlib import Path
import os
import subprocess
import tempfile
import textwrap
import re


# git search log
# git log --all --grep='admin reorder'
# git show

NEEDLE_PATH = os.environ.get("NEEDLE_PATH")
FILE_PATH = Path(settings.MEDIA_ROOT, "fastasequence_files/")


def cmdline(command):
    process = subprocess.Popen(
        args=command,
        stdout=subprocess.PIPE,
        shell=True
    )
    return process.communicate()[0]


def needle_two_sequences(file1, file2):

    cmd = NEEDLE_PATH + 'needle -datafile EBLOSUM62 -auto Y' + ' -asequence ' + \
        file1 + ' -bsequence ' + file2 + ' -sprotein1 Y -sprotein2 Y ' + ' -auto -stdout'
    print("Command line")
    print(cmd)
    results = cmdline(cmd).decode("utf-8")

    identity = re.search(r"\d{1,3}\.\d*\%", results)
    if identity:
        identity = identity.group()
        identity = identity.replace('%', '')

    return identity, results


def return_file_url(sequence):
    format_data = textwrap.fill(sequence, 80)
    tmp_seq = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
    with open(tmp_seq.name, 'wb') as temp:
        temp.write(format_data.encode())
        tmp_seq.close()
    return tmp_seq.name


def return_proteins():
    proteins = PesticidalProteinDatabase.objects.values_list(
        'name', flat=True)
    return proteins


def filtered_proteins():
    proteins = return_proteins()
    proteins_endwith1 = filter_files_ending_with_one(list(proteins))
    proteins_filtered = PesticidalProteinDatabase.objects.filter(
        name__in=proteins_endwith1)
    return proteins_filtered


def filter_files_ending_with_one(SUBJECT_FASTAFILES):
    """
    The function filters the files end with 1
    """
    return [name for name in SUBJECT_FASTAFILES if name[-1].isdigit() and not name[-2].isdigit() == 1 and int(name[-1]) == 1]


def write_files(objectname):

    for protein in objectname:
        tmp_seq = tempfile.NamedTemporaryFile(
            dir=FILE_PATH, mode="wb+", delete=False)
        fasta = textwrap.fill(protein.sequence, 80)
        str_to_write = f">{protein.name}\n{fasta}\n"
        tmp_seq.write(str_to_write.encode())
        tmp_seq.close()
        filename = os.path.basename(tmp_seq.name)
        t = PesticidalProteinDatabase.objects.get(id=protein.id)
        path_filename = "fastasequence_files/" + filename
        t.fastasequence_file = path_filename
        t.save()
    return objectname


class Command(BaseCommand):
    help = 'Runs the naming algorithm'

    def add_arguments(self, parser):
        parser.add_argument('accession', type=str,
                            help='Runs a given accession number against the list of available proteins')

    def handle(self, *args, **kwargs):
        accession_file_url = ''
        accession = kwargs['accession']
        proteins = UserSubmission.objects.filter(accession__contains=accession)
        for protein in proteins:
            accession_file_url = return_file_url(protein.sequence)
        #align = run_data.predict_name.run_bug(file_url)
        # proteins = return_proteins()
        proteins_filtered = filtered_proteins()
        protein_object = write_files(proteins_filtered)

        for protein in protein_object:
            print(protein.name)
            print(protein.fastasequence_file)

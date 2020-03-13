from database.models import PesticidalProteinDatabase
from django.conf import settings
import os
import subprocess
import re
from naming_package import naming

NEEDLE_PATH = os.environ.get("NEEDLE_PATH")


def cmdline(command):
    process = subprocess.Popen(
        args=command,
        stdout=subprocess.PIPE,
        shell=True
    )
    return process.communicate()[0]


def needle_two_sequences(file1, file2):

    needle_cline = NeedleCommandline(
        asequence=file1, bsequence=file2, gapopen=10, gapextend=0.5, outfile='stdout')

    identity = re.search(r"\d{1,3}\.\d*\%", stdout)
    if identity:
        identity = identity.group()
        identity = identity.replace('%', '')

    return identity, stdout


def blast_two_sequences(file1, file2):

    cmd = NEEDLE_PATH + 'needle -datafile EBLOSUM62 -auto Y' + ' -asequence ' + \
        file1 + ' -bsequence ' + file2 + ' -sprotein1 Y -sprotein2 Y ' + ' -auto -stdout'
    results = cmdline(cmd).decode("utf-8")

    identity = re.search(r"\d{1,3}\.\d*\%", results)
    if identity:
        identity = identity.group()
        identity = identity.replace('%', '')

    return identity, results


def filter_files_ending_with_one(SUBJECT_FASTAFILES):
    """
    The function filters the files end with 1
    """
    return [name for name in SUBJECT_FASTAFILES if name[-1].isdigit() and not name[-2].isdigit() == 1 and int(name[-1]) == 1]


def run_bug(query_data):
    PPD_proteins = PesticidalProteinDatabase.objects.exclude(
        fastasequence_file__isnull=True).exclude(fastasequence_file='').values_list('name', flat=True)
    alignResults = ''
    empty = []
    initial = 0
    align = ''
    category = ''
    name = ''
    percentageidentity = ''

    endwith1 = filter_files_ending_with_one(list(PPD_proteins))

    PPD_proteins_filtered = PesticidalProteinDatabase.objects.filter(
        name__in=endwith1)

    for protein in PPD_proteins_filtered:

        if not hasattr(protein, 'fastasequence_file'):
            continue

        #print('fastasequence_file', protein.fastasequence_file)
        s = os.path.join(settings.MEDIA_ROOT, protein.fastasequence_file.path)

        my_blast = blast_two_sequences(query_data, s)
        identity_percentage, results = my_blast

        try:
            identity_percentage = float(identity_percentage)

        except TypeError:
            print('Unable to convert identity_percentage {} for object {}'.format(
                identity_percentage, protein))
            identity_percentage = 0.0

        # this has scaffold file name , query file name and identity percentage
        l = s, query_data, identity_percentage
        # l = files[i], ordered_query_fastafiles[j], identity_percentage

        if float(l[2]) > initial:
            empty = l
            initial = float(l[2])
            align = results
            name = protein.name
            percentageidentity = l[2]

    if empty:
        # my_condition = None
        if float(empty[2]) >= 95 and float(empty[2]) <= 100:
            category = "95 to 100%"
            categories = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list('name', flat=True)
            predicted_name = naming.rank4_naming(list(categories), name)

        elif float(empty[2]) >= 76 and float(empty[2]) <= 94.9:
            category = "76 to 94%"
            categories = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list('name', flat=True)
            predicted_name = naming.rank3_naming(list(categories), name)

        elif float(empty[2]) >= 45 and float(empty[2]) <= 75.9:
            category = "45 to 75%"
            categories = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list('name', flat=True)
            predicted_name = naming.rank2_naming(list(categories), name)

        elif float(empty[2]) >= 0 and float(empty[2]) <= 44.9:
            category = "0 to 44%"
            categories = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list('name', flat=True)
            predicted_name = naming.rank1_naming(list(categories), name)

        else:
            pass

    return align, percentageidentity, category, predicted_name, name

import os
import re
import subprocess
import tempfile
import textwrap

from django.conf import settings

from database.models import (
    PesticidalProteinDatabase,
    PesticidalProteinHiddenSequence,
    PesticidalProteinPrivateDatabase,
)
from naming_package import naming

NEEDLE_PATH = os.environ.get("NEEDLE_PATH")


def cmdline(command):
    process = subprocess.Popen(
        args=command, stdout=subprocess.PIPE, shell=True)
    return process.communicate()[0]


def needle_two_sequences(file1, file2):

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
    print("Command line")
    print(cmd)
    results = cmdline(cmd).decode("utf-8")

    identity = re.search(r"\d{1,3}\.\d*\%", results)
    if identity:
        identity = identity.group()
        identity = identity.replace("%", "")

    return identity, results


def filter_files_ending_with_one(SUBJECT_FASTAFILES):
    """
    The function filters the files end with 1
    """
    return [
        name for name in SUBJECT_FASTAFILES if name[-1].isdigit() and not name[-2].isdigit() == 1 and int(name[-1]) == 1
    ]


def empty_path_private():
    proteins = PesticidalProteinPrivateDatabase.objects.all()
    for protein in proteins:
        t = PesticidalProteinPrivateDatabase.objects.get(id=protein.id)

        if t.fastasequence_file:
            os.unlink(os.path.join(settings.MEDIA_ROOT,
                                   t.fastasequence_file.name))
            t.fastasequence_file = None
            t.save()


def write_files_private(objectname):
    path = os.path.join(settings.MEDIA_ROOT + '/search_namingalgorithm/')
    # print("path", path)
    for protein in objectname:
        tmp_seq = tempfile.NamedTemporaryFile(
            suffix='.txt', dir=path, mode="wb+", delete=False)
        fasta = textwrap.fill(protein.sequence, 80)
        str_to_write = f">{protein.name}\n{fasta}\n"
        tmp_seq.write(str_to_write.encode())
        tmp_seq.close()

        filename = os.path.basename(tmp_seq.name)
        t = PesticidalProteinPrivateDatabase.objects.get(id=protein.id)
        path_filename = "fastasequence_files/" + filename
        t.fastasequence_file.name = path_filename
        t.save()


def update_private():
    private_proteins = PesticidalProteinPrivateDatabase.objects.values_list(
        "name", flat=True)
    private_endwith1 = filter_files_ending_with_one(list(private_proteins))

    private_proteins_filtered = PesticidalProteinPrivateDatabase.objects.filter(
        name__in=private_endwith1)
    write_files_private(private_proteins_filtered)


def run_bug(query_data):

    update_private()
    alignResults = ""
    empty = []
    initial = 0
    align = ""
    category = ""
    name = ""
    percentageidentity = ""

    path = os.path.join(settings.MEDIA_ROOT + '/search_namingalgorithm/*.txt')
    for file in path:
        identity_percentage, results = needle_two_sequences(query_data, file)

        try:
            identity_percentage = float(identity_percentage)

        except TypeError:
            print("Unable to convert identity_percentage {} for object {}".format(
                identity_percentage, protein))
            identity_percentage = 0.0

        # this has scaffold file name , query file name and identity percentage
        l = s, query_data, identity_percentage

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
            public = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list("name", flat=True)
            hidden = PesticidalProteinHiddenSequence.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            private = PesticidalProteinPrivateDatabase.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            categories = list(public)
            categories.extend(list(private))
            categories.extend(list(hidden))
            predicted_name = naming.rank4_naming(categories, name)

        elif float(empty[2]) >= 76 and float(empty[2]) <= 94.9:
            category = "76 to 94%"
            public = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list("name", flat=True)
            hidden = PesticidalProteinHiddenSequence.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            private = PesticidalProteinPrivateDatabase.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            categories = list(public)
            categories.extend(list(private))
            categories.extend(list(hidden))
            predicted_name = naming.rank3_naming(categories, name)

        elif float(empty[2]) >= 45 and float(empty[2]) <= 75.9:
            category = "45 to 75%"
            public = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list("name", flat=True)
            hidden = PesticidalProteinHiddenSequence.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            private = PesticidalProteinPrivateDatabase.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            categories = list(public)
            categories.extend(list(private))
            categories.extend(list(hidden))
            predicted_name = naming.rank2_naming(categories, name)

        elif float(empty[2]) >= 0 and float(empty[2]) <= 44.9:
            category = "0 to 44%"
            public = PesticidalProteinDatabase.objects.filter(
                name__startswith=name[0:3]).values_list("name", flat=True)
            hidden = PesticidalProteinHiddenSequence.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            private = PesticidalProteinPrivateDatabase.objects.filter(name__startswith=name[0:3]).values_list(
                "name", flat=True
            )
            categories = list(public)
            categories.extend(list(private))
            categories.extend(list(hidden))
            # predicted_name = naming.rank1_naming(categories, name)
            predicted_name = naming.xpp_naming(categories, name)
            # predicted_name = "Name manually"

        else:
            pass

    # remove_directory(directory)
    empty_path_private()
    return align, percentageidentity, category, predicted_name, name

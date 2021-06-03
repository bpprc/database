"""This loads the bestmatchfinder homepage."""

import logging
import os
import os.path
import re
import subprocess

from django.conf import settings
from database.models import PesticidalProteinDatabase

logger = logging.getLogger(__name__)

NEEDLE_PATH = os.environ.get("NEEDLE_PATH")


def cmdline(command):
    """This loads the bestmatchfinder homepage."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    out, error = process.communicate()
    print(error)
    return out


def blast_two_sequences(file1, file2):
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
    # print(cmd)
    results = cmdline(cmd).decode("utf-8")
    # logger.error("results of needle command line")
    # logger.error(results)
    identity = re.search(r"\d{1,3}\.\d*\%", results)
    if identity:
        identity = identity.group()
        identity = identity.replace("%", "")
    return identity, results


def run_bug(query_data):
    """This loads the bestmatchfinder homepage."""

    # PPD_proteins = PesticidalProteinDatabase.objects.exclude(fastasequence_file__isnull=True).exclude(
    #     fastasequence_file=""
    # )
    # print('DB query time', time.time() - start_time)
    # for query in query_data:
    path = os.path.join(settings.MEDIA_ROOT + '/run_bestmatchfinder/*.txt')
    empty = []
    initial = 0
    align = ""

    # take the scaffold sequence one by one
    results_list = []

    for protein in path:

        # If there is no file for this protein, ignore it.
        # if not hasattr(protein, "fastasequence_file"):
        #     continue

        # print('fastasequence_file', protein.fastasequence_file)
        # s = os.path.join(settings.MEDIA_ROOT, protein.fastasequence_file.path)
        my_blast = blast_two_sequences(query_data, protein)
        # logger.error("paths")
        # logger.error(query_data, s)
        # logger.error("\n")
        # logger.error("Blast results")
        # logger.error(my_blast)
        # logger.error("\n")
        # logger.error("\n")
        identity_percentage, results = my_blast
        # logger.error("identity_percentage")
        # logger.error(identity_percentage)
        # logger.error("\n")
        # logger.error("\n")
        # logger.error("results")
        # logger.error(results)
        # print(identity_percentage)
        # print("results", results)

        try:
            identity_percentage = float(identity_percentage)
        except TypeError:
            # print('Unable to convert identity_percentage {} for object {}'.format(identity_percentage, protein))
            identity_percentage = 0.0

        # this has scaffold file name , query file name and identity percentage
        l = protein, query_data, identity_percentage, results
        # l = protein.name, identity_percentage, results
        # l = files[i], ordered_query_fastafiles[j], identity_percentage
        results_list.append(list(l))
        if float(l[2]) > initial:
            empty = l
            initial = float(l[2])
            align = results
            # print(l)
    results_list = sorted(results_list, key=lambda x: x[2], reverse=True)[:10]
    return results_list

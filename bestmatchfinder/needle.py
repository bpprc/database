"""This loads the bestmatchfinder homepage."""

import os
import os.path
import re
import subprocess
from django.conf import settings


NEEDLE_PATH = os.environ.get("NEEDLE_PATH")
BLAST_PATH = os.environ.get("BLAST_PATH")


def cmdline(command):
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


def run_needle(file1, file2):
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
    identity = re.search(r"\d{1,3}\.\d*\%", results)
    if identity:
        identity = identity.group()
        identity = identity.replace("%", "")
    return results


def run_blast(file1, file2):
    """This loads the bestmatchfinder homepage."""

    cmd = BLAST_PATH + "blastp -query " + file1 + " -subject " + file2
    # print("cmd", cmd)
    results = cmdline(cmd).decode("utf-8")

    # f = open(settings.BASE_DIR + "/" + "demofile3.csv", "w")
    # print(settings.BASE_DIR + "/" + "demofile3.csv")
    # f.write(cmd + "\n")
    # f.write(results + "\n")
    # f.close()
    # print("type", type(results))
    # identity = re.search(r"\d{1,3}\.\d*\%", results)
    # if identity:
    #     identity = identity.group()
    #     identity = identity.replace('%', '')
    return results


def string_replace(string):
    path = os.path.join(settings.MEDIA_ROOT, "fastasequence_files/")
    empty = ''
    result = string.replace(path, empty)
    return result


def needle_alignment(file1, file2):
    """This loads the bestmatchfinder homepage."""
    results = run_needle(file1, file2)
    result = string_replace(results)
    return result


def blast_alignment(file1, file2):
    """This loads the bestmatchfinder homepage."""
    results = run_blast(file1, file2)
    result = string_replace(results)
    return result


# def run_bug(query_data):
#     """This loads the bestmatchfinder homepage."""
#     start_time = time.time()
#     PPD_proteins = PesticidalProteinDatabase.objects.exclude(fastasequence_file__isnull=True).exclude(fastasequence_file='')
#     print('DB query time', time.time() - start_time)
#     # for query in query_data:
#     empty = []
#     initial = 0
#     align = ''
#
#     #take the scaffold sequence one by one
#     for_loop_time = 0
#     start_time = time.time()
#     blast_sequence_time = 0
#     for protein in PPD_proteins:
#
#         # If there is no file for this protein, ignore it.
#         if not hasattr(protein, 'fastasequence_file'):
#             continue
#
#         #print('fastasequence_file', protein.fastasequence_file)
#         s = os.path.join(settings.MEDIA_ROOT, protein.fastasequence_file.path)
#         blast_start_time = time.time()
#         my_blast = blast_two_sequences(query_data, s)
#         blast_sequence_time += (time.time() - blast_start_time)
#         identity_percentage, results = my_blast
#
#         try:
#             identity_percentage = float(identity_percentage)
#         except TypeError:
#             print('Unable to convert identity_percentage {} for object {}'.format(identity_percentage, protein))
#             identity_percentage = 0.0
#
#         #this has scaffold file name , query file name and identity percentage
#         l = s, query_data, identity_percentage
#         # l = files[i], ordered_query_fastafiles[j], identity_percentage
#
#         if float(l[2]) > initial:
#             empty = l
#             initial = float(l[2])
#             align = results
#             #print(l)
#
#     print('For loop time', time.time() - start_time)
#     print('Blast sequence time', blast_sequence_time)
#     return align

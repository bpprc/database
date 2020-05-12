import os
import subprocess

CLUSTAL_PATH = os.environ.get("CLUSTAL_PATH")


def cmd(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    out, error = process.communicate()
    print(out, error)
    return out, error


def run_clustal(inputfile, outputfile):
    cmd_line = CLUSTAL_PATH + 'clustalo -i ' + inputfile + \
        ' --guidetree-out=' + outputfile + ' --force'
    out, error = cmd(cmd_line)
    return out

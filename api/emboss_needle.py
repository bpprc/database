#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright 2012-2018 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Python Client Automatically generated with:
# https://github.com/ebi-wp/webservice-clients-generator
#
# EMBOSS needle (REST) web service Python client using xmltramp2.
#
# For further information see:
# https://www.ebi.ac.uk/Tools/webservices/
#
###############################################################################

from __future__ import print_function

import os
import platform
import sys
import time
from optparse import OptionParser

import requests
from xmltramp2 import xmltramp

try:
    from urllib.error import HTTPError
    from urllib.parse import urlencode, urlparse
    from urllib.request import Request
    from urllib.request import __version__ as urllib_version
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode

    from urllib2 import HTTPError, Request
    from urllib2 import __version__ as urllib_version
    from urllib2 import urlopen
    from urlparse import urlparse

# allow unicode(str) to be used in python 3
try:
    unicode("")
except NameError:
    unicode = str

# Base URL for service
baseUrl = "https://www.ebi.ac.uk/Tools/services/rest/emboss_needle"
version = "2019-07-03 12:51"

# Set interval for checking status
pollFreq = 3
# Output level
outputLevel = 1
# Debug level
debugLevel = 0
# Number of option arguments.
numOpts = len(sys.argv)

# Process command-line options
parser = OptionParser(add_help_option=False)

# Tool specific options (Try to print all the commands automatically)
parser.add_option(
    "--matrix",
    type=str,
    help=("Default substitution scoring matrices."),
)
parser.add_option(
    "--gapopen",
    type=str,
    help=("Pairwise alignment score for the first residue in a gap."),
)
parser.add_option(
    "--gapext",
    type=str,
    help=("Pairwise alignment score for each additional residue in a gap."),
)
parser.add_option("--endweight", action="store_true", help=("Apply end gap penalty"))
parser.add_option(
    "--endopen",
    type=str,
    help=("Score taken away when an end gap is created."),
)
parser.add_option(
    "--endextend",
    type=str,
    help=(
        "Penalty is added to the end gap penalty for each base or residue in"
        "the end gap. This is how long end gaps are penalized."
    ),
)
parser.add_option("--format", type=str, help=("Pairwise sequences format"))
parser.add_option(
    "--stype",
    type=str,
    help=("Defines the type of the sequences to be aligned"),
)
parser.add_option(
    "--asequence",
    type=str,
    help=(
        "A free text (raw) list of sequences is simply a block of characters"
        "representing several DNA/RNA or Protein sequences. A sequence can be"
        "in GCG, FASTA, EMBL (Nucleotide only), GenBank, PIR, NBRF, PHYLIP or"
        "UniProtKB/Swiss-Prot (Protein only) format. Partially formatted"
        "sequences are not accepted. Adding a return to the end of the sequence"
        "may help certain applications understand the input. Note that directly"
        "using data from word processors may yield unpredictable results as"
        "hidden/control characters may be present."
    ),
)
parser.add_option(
    "--bsequence",
    type=str,
    help=(
        "A free text (raw) list of sequences is simply a block of characters"
        "representing several DNA/RNA or Protein sequences. A sequence can be"
        "in GCG, FASTA, EMBL (Nucleotide only), GenBank, PIR, NBRF, PHYLIP or"
        "UniProtKB/Swiss-Prot (Protein only) format. Partially formatted"
        "sequences are not accepted. Adding a return to the end of the sequence"
        "may help certain applications understand the input. Note that directly"
        "using data from word processors may yield unpredictable results as"
        "hidden/control characters may be present."
    ),
)
# General options
parser.add_option(
    "-h",
    "--help",
    action="store_true",
    help="Show this help message and exit.",
)
parser.add_option("--email", help="E-mail address.")
parser.add_option("--title", help="Job title.")
parser.add_option("--outfile", help="File name for results.")
parser.add_option("--outformat", help="Output format for results.")
parser.add_option("--asyncjob", action="store_true", help="Asynchronous mode.")
parser.add_option("--jobid", help="Job identifier.")
parser.add_option("--polljob", action="store_true", help="Get job result.")
parser.add_option(
    "--pollFreq",
    type="int",
    default=3,
    help="Poll frequency in seconds (default 3s).",
)
parser.add_option("--status", action="store_true", help="Get job status.")
parser.add_option("--resultTypes", action="store_true", help="Get result types.")
parser.add_option("--params", action="store_true", help="List input parameters.")
parser.add_option("--paramDetail", help="Get details for parameter.")
parser.add_option("--quiet", action="store_true", help="Decrease output level.")
parser.add_option("--verbose", action="store_true", help="Increase output level.")
parser.add_option(
    "--version",
    action="store_true",
    help="Prints out the version of the Client and exit.",
)
parser.add_option(
    "--debugLevel",
    type="int",
    default=debugLevel,
    help="Debugging level.",
)
parser.add_option("--baseUrl", default=baseUrl, help="Base URL for service.")

(options, args) = parser.parse_args()

# Increase output level
if options.verbose:
    outputLevel += 1

# Decrease output level
if options.quiet:
    outputLevel -= 1

# Debug level
if options.debugLevel:
    debugLevel = options.debugLevel

if options.pollFreq:
    pollFreq = options.pollFreq

if options.baseUrl:
    baseUrl = options.baseUrl


# Debug print
def printDebugMessage(functionName, message, level):
    if level <= debugLevel:
        print("[" + functionName + "] " + message, file=sys.stderr)


# User-agent for request (see RFC2616).
def getUserAgent():
    printDebugMessage("getUserAgent", "Begin", 11)
    # Agent string for urllib2 library.
    urllib_agent = "Python-urllib/%s" % urllib_version
    clientRevision = version
    # Prepend client specific agent string.
    try:
        pythonversion = platform.python_version()
        pythonsys = platform.system()
    except ValueError:
        pythonversion, pythonsys = "Unknown", "Unknown"
    user_agent = "EBI-Sample-Client/%s (%s; Python %s; %s) %s" % (
        clientRevision,
        os.path.basename(__file__),
        pythonversion,
        pythonsys,
        urllib_agent,
    )
    printDebugMessage("getUserAgent", "user_agent: " + user_agent, 12)
    printDebugMessage("getUserAgent", "End", 11)
    return user_agent


# Wrapper for a REST (HTTP GET) request
def restRequest(url):
    printDebugMessage("restRequest", "Begin", 11)
    printDebugMessage("restRequest", "url: " + url, 11)
    try:
        # Set the User-agent.
        user_agent = getUserAgent()
        http_headers = {"User-Agent": user_agent}
        req = Request(url, None, http_headers)
        # Make the request (HTTP GET).
        reqH = urlopen(req)
        resp = reqH.read()
        contenttype = reqH.info()

        if (
            len(resp) > 0
            and contenttype != "image/png;charset=UTF-8"
            and contenttype != "image/jpeg;charset=UTF-8"
            and contenttype != "application/gzip;charset=UTF-8"
        ):
            try:
                result = unicode(resp, "utf-8")
            except UnicodeDecodeError:
                result = resp
        else:
            result = resp
        reqH.close()
    # Errors are indicated by HTTP status codes.
    except HTTPError as ex:
        result = requests.get(url).content
    printDebugMessage("restRequest", "End", 11)
    return result


# Get input parameters list
def serviceGetParameters():
    printDebugMessage("serviceGetParameters", "Begin", 1)
    requestUrl = baseUrl + "/parameters"
    printDebugMessage("serviceGetParameters", "requestUrl: " + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage("serviceGetParameters", "End", 1)
    return doc["id":]


# Print list of parameters
def printGetParameters():
    printDebugMessage("printGetParameters", "Begin", 1)
    idList = serviceGetParameters()
    for id_ in idList:
        print(id_)
    printDebugMessage("printGetParameters", "End", 1)


# Get input parameter information
def serviceGetParameterDetails(paramName):
    printDebugMessage("serviceGetParameterDetails", "Begin", 1)
    printDebugMessage("serviceGetParameterDetails", "paramName: " + paramName, 2)
    requestUrl = baseUrl + "/parameterdetails/" + paramName
    printDebugMessage("serviceGetParameterDetails", "requestUrl: " + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage("serviceGetParameterDetails", "End", 1)
    return doc


# Print description of a parameter
def printGetParameterDetails(paramName):
    printDebugMessage("printGetParameterDetails", "Begin", 1)
    doc = serviceGetParameterDetails(paramName)
    print(unicode(doc.name) + "\t" + unicode(doc.type))
    print(doc.description)
    if hasattr(doc, "values"):
        for value in doc.values:
            print(value.value)
            if unicode(value.defaultValue) == "true":
                print("default")
            print("\t" + unicode(value.label))
            if hasattr(value, "properties"):
                for wsProperty in value.properties:
                    print("\t" + unicode(wsProperty.key) + "\t" + unicode(wsProperty.value))
    printDebugMessage("printGetParameterDetails", "End", 1)


# Submit job
def serviceRun(email, title, params):
    printDebugMessage("serviceRun", "Begin", 1)
    # Insert e-mail and title into params
    params["email"] = email
    if title:
        params["title"] = title
    requestUrl = baseUrl + "/run/"
    printDebugMessage("serviceRun", "requestUrl: " + requestUrl, 2)

    # Get the data for the other options
    requestData = urlencode(params)

    printDebugMessage("serviceRun", "requestData: " + requestData, 2)
    # Errors are indicated by HTTP status codes.
    try:
        # Set the HTTP User-agent.
        user_agent = getUserAgent()
        http_headers = {"User-Agent": user_agent}
        req = Request(requestUrl, None, http_headers)
        # Make the submission (HTTP POST).
        reqH = urlopen(req, requestData.encode(encoding="utf_8", errors="strict"))
        jobId = unicode(reqH.read(), "utf-8")
        reqH.close()
    except HTTPError as ex:
        print(xmltramp.parse(unicode(ex.read(), "utf-8"))[0][0])
        quit()
    printDebugMessage("serviceRun", "jobId: " + jobId, 2)
    printDebugMessage("serviceRun", "End", 1)
    return jobId


# Get job status
def serviceGetStatus(jobId):
    printDebugMessage("serviceGetStatus", "Begin", 1)
    printDebugMessage("serviceGetStatus", "jobId: " + jobId, 2)
    requestUrl = baseUrl + "/status/" + jobId
    printDebugMessage("serviceGetStatus", "requestUrl: " + requestUrl, 2)
    status = restRequest(requestUrl)
    printDebugMessage("serviceGetStatus", "status: " + status, 2)
    printDebugMessage("serviceGetStatus", "End", 1)
    return status


# Print the status of a job
def printGetStatus(jobId):
    printDebugMessage("printGetStatus", "Begin", 1)
    status = serviceGetStatus(jobId)
    if outputLevel > 0:
        print("Getting status for job %s" % jobId)
    print(status)
    if outputLevel > 0 and status == "FINISHED":
        print("To get results: python %s --polljob --jobid %s" "" % (os.path.basename(__file__), jobId))
    printDebugMessage("printGetStatus", "End", 1)


# Get available result types for job
def serviceGetResultTypes(jobId):
    printDebugMessage("serviceGetResultTypes", "Begin", 1)
    printDebugMessage("serviceGetResultTypes", "jobId: " + jobId, 2)
    requestUrl = baseUrl + "/resulttypes/" + jobId
    printDebugMessage("serviceGetResultTypes", "requestUrl: " + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage("serviceGetResultTypes", "End", 1)
    return doc["type":]


# Print list of available result types for a job.
def printGetResultTypes(jobId):
    printDebugMessage("printGetResultTypes", "Begin", 1)
    if outputLevel > 0:
        print("Getting result types for job %s" % jobId)

    resultTypeList = serviceGetResultTypes(jobId)
    if outputLevel > 0:
        print("Available result types:")
    for resultType in resultTypeList:
        print(resultType["identifier"])
        if hasattr(resultType, "label"):
            print("\t", resultType["label"])
        if hasattr(resultType, "description"):
            print("\t", resultType["description"])
        if hasattr(resultType, "mediaType"):
            print("\t", resultType["mediaType"])
        if hasattr(resultType, "fileSuffix"):
            print("\t", resultType["fileSuffix"])
    if outputLevel > 0:
        print(
            "To get results:\n  python %s --polljob --jobid %s\n"
            "  python %s --polljob --outformat <type> --jobid %s"
            ""
            % (
                os.path.basename(__file__),
                jobId,
                os.path.basename(__file__),
                jobId,
            )
        )
    printDebugMessage("printGetResultTypes", "End", 1)


# Get result
def serviceGetResult(jobId, type_):
    printDebugMessage("serviceGetResult", "Begin", 1)
    printDebugMessage("serviceGetResult", "jobId: " + jobId, 2)
    printDebugMessage("serviceGetResult", "type_: " + type_, 2)
    requestUrl = baseUrl + "/result/" + jobId + "/" + type_
    result = restRequest(requestUrl)
    printDebugMessage("serviceGetResult", "End", 1)
    return result


# Client-side poll
def clientPoll(jobId):
    printDebugMessage("clientPoll", "Begin", 1)
    result = "PENDING"
    while result == "RUNNING" or result == "PENDING":
        result = serviceGetStatus(jobId)
        if outputLevel > 0:
            print(result)
        if result == "RUNNING" or result == "PENDING":
            time.sleep(pollFreq)
    printDebugMessage("clientPoll", "End", 1)


# Get result for a jobid
# Allows more than one output file written when 'outformat' is defined.
def getResult(jobId):
    printDebugMessage("getResult", "Begin", 1)
    printDebugMessage("getResult", "jobId: " + jobId, 1)
    if outputLevel > 1:
        print("Getting results for job %s" % jobId)
    # Check status and wait if necessary
    clientPoll(jobId)
    # Get available result types
    resultTypes = serviceGetResultTypes(jobId)

    for resultType in resultTypes:
        # Derive the filename for the result
        if options.outfile:
            filename = (
                options.outfile + "." + unicode(resultType["identifier"]) + "." + unicode(resultType["fileSuffix"])
            )
        else:
            filename = jobId + "." + unicode(resultType["identifier"]) + "." + unicode(resultType["fileSuffix"])
        # Write a result file

        outformat_parm = str(options.outformat).split(",")
        for outformat_type in outformat_parm:
            outformat_type = outformat_type.replace(" ", "")

            if outformat_type == "None":
                outformat_type = None

            if not outformat_type or outformat_type == unicode(resultType["identifier"]):
                if outputLevel > 1:
                    print("Getting %s" % unicode(resultType["identifier"]))
                # Get the result
                result = serviceGetResult(jobId, unicode(resultType["identifier"]))
                if (
                    unicode(resultType["mediaType"]) == "image/png"
                    or unicode(resultType["mediaType"]) == "image/jpeg"
                    or unicode(resultType["mediaType"]) == "application/gzip"
                ):
                    fmode = "wb"
                else:
                    fmode = "w"

                try:
                    fh = open(filename, fmode)
                    fh.write(result)
                    fh.close()
                except TypeError:
                    fh.close()
                    fh = open(filename, "wb")
                    fh.write(result)
                    fh.close()
                if outputLevel > 0:
                    print("Creating result file: " + filename)
    printDebugMessage("getResult", "End", 1)


# Read a file
def readFile(filename):
    printDebugMessage("readFile", "Begin", 1)
    fh = open(filename, "r")
    data = fh.read()
    fh.close()
    printDebugMessage("readFile", "End", 1)
    return data


def print_usage():
    print(
        """\
EMBL-EBI EMBOSS needle Python Client:

Pairwise sequence alignment with Needle.

[Required (for job submission)]
  --email               E-mail address.
  --stype               Defines the type of the sequences to be aligned.
  --asequence           A free text (raw) list of sequences is simply a block of
                        characters representing several DNA/RNA or Protein
                        sequences. A sequence can be in GCG, FASTA, EMBL (Nucleotide
                        only), GenBank, PIR, NBRF, PHYLIP or UniProtKB/Swiss-Prot
                        (Protein only) format. Partially formatted sequences are not
                        accepted. Adding a return to the end of the sequence may
                        help certain applications understand the input. Note that
                        directly using data from word processors may yield
                        unpredictable results as hidden/control characters may be
                        present.
  --bsequence           A free text (raw) list of sequences is simply a block of
                        characters representing several DNA/RNA or Protein
                        sequences. A sequence can be in GCG, FASTA, EMBL (Nucleotide
                        only), GenBank, PIR, NBRF, PHYLIP or UniProtKB/Swiss-Prot
                        (Protein only) format. Partially formatted sequences are not
                        accepted. Adding a return to the end of the sequence may
                        help certain applications understand the input. Note that
                        directly using data from word processors may yield
                        unpredictable results as hidden/control characters may be
                        present.

[Optional]
  --matrix              Default substitution scoring matrices.
  --gapopen             Pairwise alignment score for the first residue in a gap.
  --gapext              Pairwise alignment score for each additional residue in a
                        gap.
  --endweight           Apply end gap penalty.
  --endopen             Score taken away when an end gap is created.
  --endextend           Penalty is added to the end gap penalty for each base or
                        residue in the end gap. This is how long end gaps are
                        penalized.
  --format              Pairwise sequences format.

[General]
  -h, --help            Show this help message and exit.
  --asyncjob            Forces to make an asynchronous query.
  --title               Title for job.
  --status              Get job status.
  --resultTypes         Get available result types for job.
  --polljob             Poll for the status of a job.
  --pollFreq            Poll frequency in seconds (default 3s).
  --jobid               JobId that was returned when an asynchronous job was submitted.
  --outfile             File name for results (default is JobId; for STDOUT).
  --outformat           Result format(s) to retrieve. It accepts comma-separated values.
  --params              List input parameters.
  --paramDetail         Display details for input parameter.
  --verbose             Increase output.
  --version             Prints out the version of the Client and exit.
  --quiet               Decrease output.
  --baseUrl             Base URL. Defaults to:
                        https://www.ebi.ac.uk/Tools/services/rest/emboss_needle

Synchronous job:
  The results/errors are returned as soon as the job is finished.
  Usage: python emboss_needle.py --email <your@email.com> [options...] <SeqFile|SeqID(s)>
  Returns: results as an attachment

Asynchronous job:
  Use this if you want to retrieve the results at a later time. The results
  are stored for up to 24 hours.
  Usage: python emboss_needle.py --asyncjob --email <your@email.com> [options...] <SeqFile|SeqID(s)>
  Returns: jobid

Check status of Asynchronous job:
  Usage: python emboss_needle.py --status --jobid <jobId>

Retrieve job data:
  Use the jobid to query for the status of the job. If the job is finished,
  it also returns the results/errors.
  Usage: python emboss_needle.py --polljob --jobid <jobId> [--outfile string]
  Returns: string indicating the status of the job and if applicable, results
  as an attachment.

Further information:
  https://www.ebi.ac.uk/Tools/webservices and
    https://github.com/ebi-wp/webservice-clients

Support/Feedback:
  https://www.ebi.ac.uk/support/"""
    )


# No options... print help.
if numOpts < 2:
    print_usage()
elif options.help:
    print_usage()
# List parameters
elif options.params:
    printGetParameters()
# Get parameter details
elif options.paramDetail:
    printGetParameterDetails(options.paramDetail)
# Print Client version
elif options.version:
    print("Revision: %s" % version)
    sys.exit()
# Submit job
elif options.email and not options.jobid:
    params = {}
    if len(args) == 1 and "true" not in args and "false" not in args:
        if os.path.exists(args[0]):  # Read file into content
            params["sequence"] = readFile(args[0])
        else:  # Argument is a sequence id
            params["sequence"] = args[0]
    elif len(args) == 2 and "true" not in args and "false" not in args:
        if os.path.exists(args[0]) and os.path.exists(args[1]):  # Read file into content
            params["asequence"] = readFile(args[0])
            params["bsequence"] = readFile(args[1])
        else:  # Argument is a sequence id
            params["asequence"] = args[0]
            params["bsequence"] = args[0]
    elif hasattr(options, "sequence") or (
        hasattr(options, "asequence") and hasattr(options, "bsequence")
    ):  # Specified via option
        if hasattr(options, "sequence"):
            if os.path.exists(options.sequence):  # Read file into content
                params["sequence"] = readFile(options.sequence)
            else:  # Argument is a sequence id
                params["sequence"] = options.sequence
        elif hasattr(options, "asequence") and hasattr(options, "bsequence"):
            if os.path.exists(options.asequence) and os.path.exists(options.bsequence):  # Read file into content
                params["asequence"] = readFile(options.asequence)
                params["bsequence"] = readFile(options.bsequence)
            else:  # Argument is a sequence id
                params["asequence"] = options.asequence
                params["bsequence"] = options.bsequence

    # Pass default values and fix bools (without default value)
    if options.stype:
        params["stype"] = options.stype

    if options.matrix:
        params["matrix"] = options.matrix

    if not options.gapopen:
        params["gapopen"] = "10"
    if options.gapopen:
        params["gapopen"] = options.gapopen

    if not options.gapext:
        params["gapext"] = "0.5"
    if options.gapext:
        params["gapext"] = options.gapext

    if not options.endweight:
        params["endweight"] = "false"
    if options.endweight:
        params["endweight"] = options.endweight

    if not options.endopen:
        params["endopen"] = "10"
    if options.endopen:
        params["endopen"] = options.endopen

    if not options.endextend:
        params["endextend"] = "0.5"
    if options.endextend:
        params["endextend"] = options.endextend

    if not options.format:
        params["format"] = "pair"
    if options.format:
        params["format"] = options.format

    # Submit the job
    jobId = serviceRun(options.email, options.title, params)
    if options.asyncjob:  # Async mode
        print(jobId)
        if outputLevel > 0:
            print("To check status: python %s --status --jobid %s" "" % (os.path.basename(__file__), jobId))
    else:
        # Sync mode
        if outputLevel > 0:
            print("JobId: " + jobId, file=sys.stderr)
        else:
            print(jobId)
        time.sleep(pollFreq)
        getResult(jobId)
# Get job status
elif options.jobid and options.status:
    printGetStatus(options.jobid)

elif options.jobid and (options.resultTypes or options.polljob):
    status = serviceGetStatus(options.jobid)
    if status == "PENDING" or status == "RUNNING":
        print("Error: Job status is %s. " "To get result types the job must be finished." % status)
        quit()
    # List result types for job
    if options.resultTypes:
        printGetResultTypes(options.jobid)
    # Get results for job
    elif options.polljob:
        getResult(options.jobid)
else:
    # Checks for 'email' parameter
    if not options.email:
        print('\nParameter "--email" is missing in your command. It is required!\n')

    print("Error: unrecognised argument combination", file=sys.stderr)
    print_usage()

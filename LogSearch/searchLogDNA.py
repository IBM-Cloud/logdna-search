#!/usr/bin/python3
# Simple Python script to search LogDNA entries and thereby exporting them
#
# Written by Henrik Loeser, IBM, hloeser@de.ibm.com

import requests, json, sys
from datetime import timedelta, datetime, tzinfo, timezone

# load the configuration file with region and service key info
def loadConfig(filename):
    with open(filename) as data_file:
        logConfig = json.load(data_file)
    return logConfig

# perform the actual search
def getLogs(region, key, numHours, query):
    url     = "https://api."+region+".logging.cloud.ibm.com/v1/export"
    params = {
        "from": datetime.timestamp(datetime.now())-(3600*int(numHours)),
        "to": datetime.timestamp(datetime.now()),
        "query": query,
        "size": "10000"
        }
    response  = requests.get( url, auth=(key,''), params=params)
    # the result are lines of JSON, so store them individually
    result = [json.loads(jline) for jline in response.text.splitlines()]
    return result

def printHelp(progname):
    print ("Usage: "+progname+" config [hours] [query]")
    print ("   config: name of configuration file")
    print ("   hours:  number of hours back from now")
    print ("   query:  search term(s) as string")


# Get started by going over the parameters
if __name__== "__main__":
    if (len(sys.argv)<2):
        printHelp(sys.argv[0])
        exit()
    else:
        # we definitely expect a config file
        logConfig=loadConfig(sys.argv[1])
        # no query by default
        query=""
        # 48 hours by default
        numHours=48
    if (len(sys.argv)==3):
        numHours=sys.argv[2]
    elif (len(sys.argv)==4):
        numHours=sys.argv[2]
        query=sys.argv[3]
    else:
        printHelp(sys.argv[0])
        exit()

    # Obtain the LogDNA logs
    logs=getLogs(logConfig["region"],logConfig["key"],numHours, query)
    # Because the result are loglines (JSONL), we need to dump each one individually
    [print (json.dumps(jsonl, indent=2)) for jsonl in logs]
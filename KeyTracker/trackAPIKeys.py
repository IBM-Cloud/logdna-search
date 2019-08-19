#!/usr/bin/python3
# Track usage of IBM Cloud API keys using Activity Tracker with LogDNA
# 
# The script makes us of the LogDNA export API and the IBM Cloud IAM
# Identity Services API
#
# (c) 2019 IBM, written by Henrik Loeser
import requests, json, sys
from datetime import timedelta, datetime, tzinfo, timezone


iamInfoUrl="https://iam.cloud.ibm.com/identity/.well-known/openid-configuration"

# Read the credentials from the provided file
def readApiKey(filename):
    with open(filename) as data_file:
        credentials = json.load(data_file)
    return credentials

# Log in to IBM Cloud using the API key
def getAuthTokens(api_key):
    url     = "https://iam.cloud.ibm.com/identity/token"
    headers = { "Content-Type" : "application/x-www-form-urlencoded" }
    data    = "apikey=" + api_key + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response  = requests.post( url, headers=headers, data=data )
    return response.json()

# Obtain details on the API key, including the account ID
def getIAMDetails(api_key, iam_token):
    url     = "https://iam.cloud.ibm.com/v1/apikeys/details"
    headers = { "Authorization" : "Bearer "+iam_token, "IAM-Apikey" : api_key, "Content-Type" : "application/json" }
    response  = requests.get( url, headers=headers )
    return response.json()

# Request the list of API keys
def getApiKeys(iam_token, account_id, iam_id):
    url = 'https://iam.cloud.ibm.com/v1/apikeys'
    headers = { "Authorization" : "Bearer "+iam_token }
    payload = {"account_id": account_id, "iam_id": iam_id}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

# Obtain the list of service IDs for the account
def getServiceIDs(iam_token, account_id):
    url = 'https://iam.cloud.ibm.com/v1/serviceids'
    headers = { "Authorization" : "Bearer "+iam_token }
    payload = {"account_id": account_id, "pagesize": 100}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

# perform the LogDNA search
def getLogs(region, key, numHours, query):
    url     = "https://api."+region+".logging.cloud.ibm.com/v1/export"
    # could use some improvements, size is hardcoded
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
    print ("Usage: "+progname+" credential-file")

# Script flow starts here
if __name__== "__main__":
    credfile=None
    # process parameter(s)
    if (len(sys.argv)<2):
        printHelp(sys.argv[0])
        exit()
    elif (len(sys.argv)==2):
        credfile=sys.argv[1]
    else:
        print ("unknown options")
        printHelp(sys.argv[0])
        exit()

    
    # Reading credentials
    credentials=readApiKey(credfile)
    apiKey=credentials.get('apiKey')
    logRegion=credentials.get('region')
    logKey=credentials.get('key')

    # generating auth tokens
    authTokens=getAuthTokens(api_key=apiKey)
    iam_token=authTokens["access_token"]   

    # Getting account details details
    accDetails=getIAMDetails(api_key=apiKey, iam_token=iam_token)
    account_id=accDetails['account_id']

    # Getting API keys
    api_key_list=getApiKeys(iam_token=iam_token, account_id=account_id, iam_id=accDetails['iam_id'])
    
    #
    # Obtain the LogDNA logs for the user
    #
    
    # When is this report generated...?
    json_report={"generated_at": str(datetime.now())}
    json_report["apikeys"]=[]
    # Go over the list of API keys
    for aKey in api_key_list['apikeys']:
        jk={}
        jk["name"]=aKey["name"]
        jk["created_at"]=aKey["created_at"]
        # search for 30 days (24 hours * 30)
        logs=getLogs(logRegion,logKey,720, aKey['name']+" AND "+aKey["iam_id"])
        numlogs=len(logs)
        jk["numlogs"]=numlogs
        # assuming the records are ordered ascending
        if numlogs>0:
            jk["lastEventTime"]=logs[numlogs-1]["eventTime"]
        #print(json.dumps(jk, indent=2))
        json_report["apikeys"].append(jk)

    # repeat for service IDs
    service_id_list=getServiceIDs(iam_token, account_id)
    json_report["serviceids"]=[]
    for serviceID in service_id_list["serviceids"]:
        jsid={}
        jsid["name"]=serviceID["name"]
        jsid["created_at"]=serviceID["created_at"]
        jsid["keys"]=[]
        # get list of API keys for the current service ID
        api_key_list=getApiKeys(iam_token, account_id, serviceID["iam_id"])
        # similar to above, process the API keys
        for aKey in api_key_list['apikeys']:
            jk={}
            jk["name"]=aKey["name"]
            jk["created_at"]=aKey["created_at"]

            logs=getLogs(logRegion,logKey,720, aKey['name']+" AND "+aKey["iam_id"])
            numlogs=len(logs)
            jk["numlogs"]=numlogs
            if numlogs>0:
                jk["lastEventTime"]=logs[numlogs-1]["eventTime"]
            jsid["keys"].append(jk)
        #print(json.dumps(jsid, indent=2))
        json_report["serviceids"].append(jsid)

    # all done, now dump the report
    print(json.dumps(json_report, indent=2))


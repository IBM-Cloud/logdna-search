# Track usage of IBM Cloud API keys

This is a sample Python tool to search [Activity Tracker with LogDNA service on IBM Cloud](https://cloud.ibm.com/docs/services/Activity-Tracker-with-LogDNA?topic=logdnaat-getting-started) for usage of API keys. It utilizes the [IAM Identity Services API](https://cloud.ibm.com/apidocs/iam-identity-token-api#introduction) to obtain a list of personal API keys as well as keys for account service IDs.

## Setup

Copy over the file [creds.sample.json](creds.sample.json) to, e.g., credsEU.json. Edit the file and adapt it to the region (us-south, eu-de, ...) and add your LogDNA service key as well as a valid API key. [The LogDNA service key can be obtained in the LogDNA UI following these documented steps](https://cloud.ibm.com/docs/services/Activity-Tracker-with-LogDNA?topic=logdnaat-export#export_step3). An [IBM Cloud API key can be created on this page](https://cloud.ibm.com/iam/apikeys) or on the command line.

## Usage

The [trackAPIKeys.py](trackAPIKeys.py) tool is invoked with the name of the credentials file as parameter. Usage information is printed if no parameters is provided:

```
./trackAPIKeys.py credsEU.json
```

It returns a JSON document with information per individual key. The tool is discussed in the IBM Cloud blog post [Improve Security: Track API Keys Using IAM and LogDNA](https://www.ibm.com/cloud/blog/improve-security-track-api-keys-using-iam-and-logdna). The post includes a screenshot with sample output.

# License

See [LICENSE](/LICENSE) for license information.

The tool is provided on a "as-is" basis and is un-supported. Use with care...

# Contribute

To contribute, please open a [Pull Request](/pulls).
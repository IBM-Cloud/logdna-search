# Search and export LogDNA entries

This is a sample Python tool to search and export JSONL records from [Activity Tracker with LogDNA service on IBM Cloud](https://cloud.ibm.com/docs/services/Activity-Tracker-with-LogDNA?topic=logdnaat-getting-started).

## Setup

Copy over the file [logConfig.sample.json](logConfig.sample.json) to, e.g., logConfigEU.json. Edit the file and adapt it to the region (us-south, eu-de, ...) and add your LogDNA service key. [The key can be obtained in the LogDNA UI following these documented steps](https://cloud.ibm.com/docs/services/Activity-Tracker-with-LogDNA?topic=logdnaat-export#export_step3).

## Usage

The sample tool is invoked with one mandatory and two optional parameters. Usage information is printed if no parameters is provided:

```
Usage: searchLogDNA.py config [hours] [query]
   config: name of configuration file
   hours:  number of hours back from now
   query:  search term(s) as string
```

- The tool requires a configuration (see above) to be provided.
- It can be followed by the number of hours to go back in the search history. The default is 48 hours.
- The last parameter is an optional query string (see [LogDNA search syntax](https://docs.logdna.com/docs/search)).


### Sample searches

Search within the past hour for entries having a value starting with "python":

`searchLogDNA.py logConfigEU.json 1 python`


Search the past 24 hours for initiator names "hloeser:

`searchLogDNA.py logConfigEU.json 24 'initiator.name:hloeser'`

### Combine with jq

Combine the search tool with the [jq](https://stedolan.github.io/jq/) command to filter down the records to the actual logline.

`searchLogDNA.py logConfigEU.json 24 'initiator.name:hloeser' | jq -r '._line'`

Go even deeper and look only for the initiator:

`searchLogDNA.py logConfigEU.json 24 'initiator.name:hloeser' | jq -r '._line' | jq -r '.initiator'`

# License

See [LICENSE](/LICENSE) for license information.

The tool is provided on a "as-is" basis and is un-supported. Use with care...

# Contribute

To contribute, please open a [Pull Request](/pulls).
# Use Activity Tracker with LogDNA to analyze account activity

This repository contains sample Python code that demonstrates the use of IBM Cloud Actvity Tracker with LogDNA. It includes the following tools:

- [LogSearch](LogSearch): The Python script in this directory uses the LogDNA export API to search and extract activity logs.
- [KeyTracker](KeyTracker): Based on LogSearch functionality, this small tool first obtains lists of active IBM Cloud platform API keys and API keys for service IDs, then searches LogDNA for the API key usage. If found, the number of log lines and the timestamp of the most recent usage are returned in a JSON-based report.

# License

See [LICENSE](/LICENSE) for license information.

The tool is provided on a "as-is" basis and is un-supported. Use with care...

# Contribute

To contribute, please open a [Pull Request](/pulls).

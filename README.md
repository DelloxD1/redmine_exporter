# Overview
This Python script is designed to interact with Redmine, a project management application, and generate a summary of project issues. It uses the Redmine API to retrieve and process data, and outputs the results in a prometheus metrics format. The script is designed to be flexible and configurable, allowing users to specify various parameters such as the Redmine URL, version, username, password, token, and the number of days to consider when fetching data.

### **It's designed be used in combination with the Textfile Collector of the node_exporter!** 

# Dependencies
The script requires the following Python libraries:

- `redminelib`: A Python library for interacting with the [Redmine API](https://python-redmine.com/).
- `argparse`: A Python library for writing user-friendly command-line interfaces.
- `yaml`: A Python library for parsing YAML files.
- `time`: A Python library for time-related functions.
- `datetime`: A Python library for working with dates and times.
# Usage
The script is intended to be run from the command line and requires a configuration file as an argument. The configuration file should be a YAML file containing the necessary parameters for connecting to the Redmine server and specifying the projects and users to consider.

Here's an example of how to run the script:

```
python3 script.py --config config.yaml
```
The `config.yaml` file might look something like this:

```
redmine:
 url: http://demo.redmine.org
 version: 3.4.5
 username: admin
 password: admin
 token: 1234567890abcdef
 get_last_timedelta_days: 7
projects:
 - project1
 - project2
users:
 - user1
 - user2
```
# Functionality
The script defines several functions for interacting with the Redmine API:

- `get_total_project_issues(project, closed_on=None, created_on=None, status="open")`: Retrieves the total number of issues for a given project, optionally filtered by status and date.
- `get_user_id(user)`: Retrieves the ID of a given user.
- `get_userspecific_issues(user, status)`: Retrieves the total number of issues assigned to a given user, filtered by status.
- `last_days(days, project, status=None)`: Retrieves the total number of issues created in the last days days for a given project, optionally filtered by status.
The script then prints out a series of metrics for each project and user, including the total number of open and closed issues, the number of issues created today, and the number of issues assigned to each user.

# Output
The script outputs a series of Prometheus-style metrics, which can be scraped by a Prometheus server. Each metric includes a help string and a type declaration, followed by a series of data points for each project and user.

Here's an example of the output:
```
# HELP redmine_opened_project_issues_last_7 A summary of open tickets within the last 7 days per project
# TYPE redmine_opened_project_issues_last_7 gauge
redmine_opened_project_issues_last_7_days{project="project1"} 10
redmine_opened_project_issues_last_7_days{project="project2"} 5
...
```
# Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.
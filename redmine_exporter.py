#!/usr/bin/env python3
from redminelib import Redmine
import argparse
import yaml
import time
from datetime import datetime, date, timedelta

# Measure the execution time of the script
start_time = time.time()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True, help='path of the configfile')
args = parser.parse_args()

# Load configuration from YAML file
config = yaml.safe_load(open(args.config))

# Extract Redmine configuration parameters
url = config.get('redmine', {}).get('url', 'NA')
version = config.get('redmine', {}).get('version', 'NA')
username = config.get('redmine', {}).get('username', 'NA')
password = config.get('redmine', {}).get('password', 'NA')
token = config.get('redmine', {}).get('token', 'NA')
timedelta_days = config.get('redmine', {}).get('get_last_timedelta_days', 'NA')
projects = config.get('projects')
users = config.get('users')

# Create Redmine connection object based on token or username/password
if config.get('redmine', {}).get('token', 'NA'):
    redmine = Redmine(url, version=version, key=token)
else:
    redmine = Redmine(url, version=version, username=username, password=password)

# Function to get the total number of issues for a project
def get_total_project_issues(project, closed_on=None, created_on=None, status="open"):
    issues = redmine.issue.filter(
        project_id=project,
        status_id=status,
        closed_on=closed_on,
        created_on=created_on
    )
    return len(issues)

# Function to get the user ID based on the username
def get_user_id(user):
    userid = list(redmine.user.filter(name=user))
    return userid[0].id

# Function to get the number of issues assigned to a user with a specific status
def get_userspecific_issues(user, status):
    issues = redmine.issue.filter(
        assigned_to_id=user,
        status_id=status
    )
    return len(issues)

# Function to get the number of issues created in the last 'days' days for a project
def last_days(days, project, status=None):
    today = date.today()
    counter = 0
    for i in range(days):
        d = today - timedelta(days=i)
        counter = counter + get_total_project_issues(created_on=d, project=project, status=status)
    return counter

# Print Prometheus-style metrics for open and closed issues per project
print("# HELP redmine_opened_project_issues_last_" + str(timedelta_days) + " A summary of open tickets within the last " + str(timedelta_days) + " days per project")
print("# TYPE redmine_opened_project_issues_last_" + str(timedelta_days) + " gauge")
for project in projects:
    print("redmine_opened_project_issues_last_" + str(timedelta_days) + "_days" + '{project="'+ project.replace("-","_") + '"} ' + str(last_days(timedelta_days, project, status="*")))

print("# HELP redmine_closed_project_issues_last_" + str(timedelta_days) + " A summary of closed tickets within the last " + str(timedelta_days) + " days per project")
print("# TYPE redmine_closed_project_issues_last_" + str(timedelta_days) + " gauge")
for project in projects:
    print("redmine_closed_project_issues_last_" + str(timedelta_days) + "_days" + '{project="'+ project.replace("-","_") + '"} ' + str(last_days(timedelta_days, project, status="closed")))

# Print Prometheus-style metrics for total open issues per project
print("# HELP redmine_total_open_project_issues A summary of open tickets per project")
print("# TYPE redmine_total_open_project_issues gauge")
for project in projects:
    print("redmine_total_open_project_issues" + '{project="'+ project.replace("-","_") + '"} ' + str(get_total_project_issues(project)))

# Print Prometheus-style metrics for open and closed issues per project created/closed today
print("# HELP redmine_opened_project_issues_today A summary of all opened tickets per project today")
print("# TYPE redmine_opened_project_issues_today gauge")
for project in projects:
    print("redmine_opened_project_issues_today" + '{project="'+ project.replace("-","_") + '"} ' + str(get_total_project_issues(project, status=None, created_on=datetime.today().date())))

print("# HELP redmine_closed_project_issues_today A summary of all closed tickets per project today")
print("# TYPE redmine_closed_project_issues_today gauge")
for project in projects:
    print("redmine_closed_project_issues_today" + '{project="'+ project.replace("-","_") + '"} ' + str(get_total_project_issues(project, status="closed", closed_on=datetime.today().date())))

# Print Prometheus-style metrics for open issues per user
print("# HELP redmine_open_user_issues A summary of all open tickets per user")
print("# TYPE redmine_open_user_issues gauge")
for user in users:
    print("redmine_open_user_issues" + '{user="'+ user.replace("-","_") + '"} ' + str(get_userspecific_issues(get_user_id(user), status="open")))
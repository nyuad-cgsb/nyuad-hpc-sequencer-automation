from jira import JIRA, JIRAError
from pprint import pprint
import os

"""WIP
Phase 2 will be to use the JIRA API to update tickets
For right now there is just the skeleton
"""


def read(file_path):
    """ Read a file and return it's contents. """
    with open(file_path) as f:
        return f.read()


key_cert = os.path.join(os.path.expanduser('~'), '.ssh', 'jira.pem')
RSA_KEY = read(key_cert)

# The Consumer Key created while setting up the "Incoming Authentication" in
# JIRA for the Application Link.
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
JIRA_SERVER = os.environ.get('JIRA_SERVER')
oauth_token = os.environ.get('OAUTH_TOKEN')
oauth_token_secret = os.environ.get('OAUTH_TOKEN_SECRET')

jira_client = JIRA(options={'server': JIRA_SERVER}, oauth={
    'access_token': oauth_token,
    'access_token_secret': oauth_token_secret,
    'consumer_key': CONSUMER_KEY,
    'key_cert': RSA_KEY
})

# # print all of the project
# for project in jira_client.projects():
#     print(project.key)
#
# issue_dict = {
#     'project': 'NCS',
#     'summary': 'New issue from jira-python',
#     'description': 'THIS IS A TEST. IT IS ONLY A TEST. DO NOT BE ALARMED',
#     'issuetype': {'name': 'Task'},
# }
# new_issue = jira_client.create_issue(fields=issue_dict)
# # pprint(new_issue)
#
# try:
#     issue = jira_client.issue(id='NCS-174')
#     summary = issue.fields.summary
#     description = issue.fields.description
#     pprint(issue)
# except JIRAError as jira_error:
#     pprint(jira_error)
#     print(str(jira_error))
# except Exception as e:
#     print('hello')

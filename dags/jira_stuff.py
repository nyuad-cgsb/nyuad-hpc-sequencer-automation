from jira import JIRA
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

# Now you can use the access tokens with the JIRA client. Hooray!
jira = JIRA(options={'server': JIRA_SERVER}, oauth={
    'access_token': oauth_token,
    'access_token_secret': oauth_token_secret,
    'consumer_key': CONSUMER_KEY,
    'key_cert': RSA_KEY
})

# print all of the project keys just as an exmaple
for project in jira.projects():
    print(project.key)

issue_dict = {
    'project': 'NCS',
    'summary': 'New issue from jira-python',
    'description': 'THIS IS A TEST. IT IS ONLY A TEST. DO NOT BE ALARMED',
    'issuetype': {'name': 'Task'},
}
new_issue = jira.create_issue(fields=issue_dict)

pprint(new_issue)

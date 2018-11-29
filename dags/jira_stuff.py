from jira import JIRA
import re
from pprint import pprint


def read(file_path):
    """ Read a file and return it's contents. """
    with open(file_path) as f:
        return f.read()

# The contents of the rsa.pem file generated (the private RSA key)
key_cert = '/Users/jillian/.ssh/jira.pem'
RSA_KEY = read(key_cert)

# The Consumer Key created while setting up the "Incoming Authentication" in
# JIRA for the Application Link.
CONSUMER_KEY = 'jira-cli'
JIRA_SERVER = 'https://cbi.abudhabi.nyu.edu/jira'
oauth_token = '1T1xc0MJUnBvHKA0o8D1IMR3ph90X278'
oauth_token_secret = 'hHXVLpnrX64XjTRNEdPEjg1eaS3KpRev'

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

import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session
from jira.client import JIRA


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
CONSUMER_SECRET = 'dont_care'
VERIFIER = 'jira_verifier'

# The URLs for the JIRA instance
JIRA_SERVER = 'https://cbi.abudhabi.nyu.edu/jira'
REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'

# Step 1: Get a request token
oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY)
request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL)

resource_owner_key = request_token['oauth_token']
resource_owner_secret = request_token['oauth_token_secret']

print("STEP 1: GET REQUEST TOKEN")
print("  oauth_token={}".format(resource_owner_key))
print("  oauth_token_secret={}".format(resource_owner_secret))
print("\n")

# Step 2: Get the end-user's authorization
print("STEP2: AUTHORIZATION")
print("  Visit to the following URL to provide authorization:")
print("  {}?oauth_token={}".format(AUTHORIZE_URL, request_token['oauth_token']))
print("\n")

input("Press any key to continue...")

oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret, verifier=VERIFIER, signature_method=SIGNATURE_RSA,
                      rsa_key=RSA_KEY)

# Step 3: Get the access token
access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)

print("STEP2: GET ACCESS TOKEN")
print("  oauth_token={}".format(access_token['oauth_token']))
print("  oauth_token_secret={}".format(access_token['oauth_token_secret']))
print("\n")

oauth_token = '1T1xc0MJUnBvHKA0o8D1IMR3ph90X278'
oauth_token_secret = 'hHXVLpnrX64XjTRNEdPEjg1eaS3KpRev'

# Now you can use the access tokens with the JIRA client. Hooray!
jira = JIRA(options={'server': JIRA_SERVER}, oauth={
    'access_token': access_token['oauth_token'],
    'access_token_secret': access_token['oauth_token_secret'],
    'consumer_key': CONSUMER_KEY,
    'key_cert': RSA_KEY
})

# print all of the project keys just as an exmaple
for project in jira.projects():
    print(project.key)

# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, jsonify, request
import json
from airflow.www.app import csrf
from nyuad_cgsb_jira_client.jira_client import jira_client
from jira import JIRAError


JIRABlueprint = Blueprint(
    'jira', __name__,
    url_prefix='/jira'
)


@JIRABlueprint.route('/get_jira_ticket', methods=['POST'])
@csrf.exempt
def get_jira_ticket():
    """Adds localhost:8080/jira"""
    request_data = json.loads(request.data.decode('utf-8'))
    ticket_id = request_data.get('ticketId')
    results = {}
    try:
        issue = jira_client.issue(id=ticket_id)
        results['id'] = ticket_id
        results['summary'] = issue.fields.summary
        results['description'] = issue.fields.description
    except JIRAError as jira_error:
        results['error'] = str(jira_error)
    except Exception as e:
        results['error'] = str(e)
    return jsonify(results)


@JIRABlueprint.route('/create_jira_ticket', methods=['POST'])
@csrf.exempt
def create_jira():
    """Adds localhost:8080/jira/create_jira"""
    request_data = json.loads(request.data.decode('utf-8'))
    issue_dict = {
        'project': 'NCS',
        'summary': request_data.get('summary'),
        'description': request_data.get('description'),
        'issuetype': {'name': 'Task'},
    }
    results = {}
    try:
        issue = jira_client.create_issue(fields=issue_dict)
        results['id'] = issue.key
        results['summary'] = issue.fields.summary
        results['description'] = issue.fields.description
    except JIRAError as jira_error:
        results['error'] = str(jira_error)
    except Exception as e:
        results['error'] = str(e)

    return jsonify(results)


# Defining the plugin class
class JiraPlugin(AirflowPlugin):
    name = "jira_plugin"
    operators = []
    sensors = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = [JIRABlueprint]
    menu_links = []

# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint, jsonify, request
from airflow.www.app import csrf


JIRABlueprint = Blueprint(
    'jira', __name__,
    url_prefix='/jira'
)


@JIRABlueprint.route('/', methods=['GET'])
@csrf.exempt
def serve_metrics():
    """Adds localhost:8080/jira"""
    return jsonify({'hello': 'world'})


@JIRABlueprint.route('/create_jira', methods=['GET'])
@csrf.exempt
def create_jira():
    """Adds localhost:8080/jira/create_jira"""
    return jsonify({'hello': 'world'})


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

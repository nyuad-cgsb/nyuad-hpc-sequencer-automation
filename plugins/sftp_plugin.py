from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, jsonify, request
import os
import fnmatch
import json
from airflow.www.app import csrf
from ssh_helpers import initialize_ssh
from demultiplex.ensure_samplesheet import ensure_valid_csv_file

SFTPBlueprint = Blueprint(
    'sftp', __name__,
    url_prefix='/sftp'
)


@SFTPBlueprint.route('/does_file_exist', methods=['POST'])
@csrf.exempt
def does_file_exist():
    """Adds localhost:8080/sftp/does_file_exist/
    Check to see if a file exists
    SFTP will throw an error if the directory doesn't exist
    So we wrap this in a try/catch block
    """
    request_data = json.loads(request.data.decode('utf-8'))
    file = request_data.get('file')
    dir = os.dirname(file)
    ssh, sftp = initialize_ssh('gencore', 'dalma.abudhabi.nyu.edu')
    results = {}
    results['dir_exists'] = False
    files = []
    try:
        files = sftp.listdir(dir)
        results['dir_exists'] = True
    except FileNotFoundError as e:
        files = []
        results['dir_exists'] = False
        results['error'] = str(e)

    if file in files:
        results['file_exists'] = True
    else:
        results['file_exists'] = False

    return jsonify({'results': results, 'context': {'endpoint': '/sftp/does_file_exist', 'args': request_data}})


@SFTPBlueprint.route('/does_dir_exist', methods=['POST'])
@csrf.exempt
def does_dir_exist():
    """Adds localhost:8080/sftp/does_dir_exist/
    Check to see if a directory exists
    SFTP will throw an error if the directory doesn't exist
    So we wrap this in a try/catch block
    """
    request_data = json.loads(request.data.decode('utf-8'))
    dir = request_data.get('dir')
    ssh, sftp = initialize_ssh('gencore', 'dalma.abudhabi.nyu.edu')
    results = {}
    results['dir_exists'] = False
    try:
        sftp.listdir(dir)
        results['dir_exists'] = True
    except FileNotFoundError as e:
        results['dir_exists'] = False
        results['error'] = str(e)

    return jsonify({'results': results, 'context': {'endpoint': '/sftp/does_dir_exist', 'args': request_data}})

# TODO Add sample_sheet_is_valid to REST API

# Defining the plugin class
class SFTPPlugin(AirflowPlugin):
    name = "sftp_plugin"
    operators = []
    sensors = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = [SFTPBlueprint]
    menu_links = []

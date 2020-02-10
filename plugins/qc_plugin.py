from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, jsonify, request
import fnmatch
import json
from airflow.www.app import csrf
from ssh_helpers import initialize_ssh

GetQCProdWorkflowsBlueprint = Blueprint(
    'qc', __name__,
    url_prefix='/qc'
)


@GetQCProdWorkflowsBlueprint.route('/health', methods=['GET'])
@csrf.exempt
def health():
    """Adds localhost:8080/qc/health
    This is just a health endpoint
    """
    return jsonify({'hello': 'world', 'context': {'endpoint': '/qc/health', 'args': {}}})


@GetQCProdWorkflowsBlueprint.route('/get_qc_workflows', methods=['GET'])
@csrf.exempt
def get_qc_workflows():
    """Adds localhost:8080/qc/get_qc_prod_workflows
    This is simply a rest api that returns the workflows in /scratch/gencore/production that match QC
    """

    ssh, sftp = initialize_ssh('gencore', 'dalma.abudhabi.nyu.edu')
    qc_workflows = []
    dir = '/scratch/gencore/workflows/production/'
    for filename in sftp.listdir(dir):
        if fnmatch.fnmatch(filename, "*QC*yml") or fnmatch.fnmatch(filename, "*qc*yml"):
            qc_workflows.append('{}{}'.format(dir, filename))
    dir = '/scratch/gencore/workflows/stable/'
    for filename in sftp.listdir(dir):
        if fnmatch.fnmatch(filename, "*QC*yml") or fnmatch.fnmatch(filename, "*qc*yml"):
            qc_workflows.append('{}{}'.format(dir, filename))
    return jsonify({'qc_workflows': qc_workflows, 'context': {'endpoint': '/qc/get_qc_workflows', 'args': {}}})


@GetQCProdWorkflowsBlueprint.route('/get_qc_prod_workflows', methods=['GET'])
@csrf.exempt
def get_qc_prod_workflows():
    """Adds localhost:8080/qc/get_qc_prod_workflows
    This is simply a rest api that returns the workflows in /scratch/gencore/production that match QC
    """

    ssh, sftp = initialize_ssh('gencore', 'dalma.abudhabi.nyu.edu')
    qc_workflows = []
    dir = '/scratch/gencore/workflows/production/'
    for filename in sftp.listdir(dir):
        if fnmatch.fnmatch(filename, "*QC*yml") or fnmatch.fnmatch(filename, "*qc*yml"):
            qc_workflows.append('{}{}'.format(dir, filename))
    return jsonify({'qc_workflows': qc_workflows, 'context': {'endpoint': '/qc/get_qc_prod_workflows', 'args': {}}})


@GetQCProdWorkflowsBlueprint.route('/get_qc_stable_workflows', methods=['GET'])
@csrf.exempt
def get_qc_stable_workflows():
    """Adds localhost:8080/qc/get_qc_stable_workflows
    This is simply a rest api that returns the workflows in /scratch/gencore/stable that match QC
    """

    ssh, sftp = initialize_ssh('gencore', 'dalma.abudhabi.nyu.edu')
    qc_workflows = []
    dir = '/scratch/gencore/workflows/stable/'
    for filename in sftp.listdir(dir):
        if fnmatch.fnmatch(filename, "*QC*yml") or fnmatch.fnmatch(filename, "*qc*yml"):
            qc_workflows.append('{}{}'.format(dir, filename))
    return jsonify({'qc_workflows': qc_workflows, 'context': {'endpoint': '/qc/get_qc_stable_workflows', 'args': {}}})


# Defining the plugin class
class QCPlugin(AirflowPlugin):
    name = "qc_plugin"
    operators = []
    sensors = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = [GetQCProdWorkflowsBlueprint]
    menu_links = []

# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_admin import BaseView, expose
from flask_admin.base import MenuLink

# Importing base classes that we need to derive
from airflow.hooks.base_hook import BaseHook
from airflow.models import BaseOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.executors.base_executor import BaseExecutor


# Will show up under airflow.hooks.test_plugin.PluginHook
class PluginHook(BaseHook):
    pass


# Will show up under airflow.operators.test_plugin.PluginOperator
class PluginOperator(BaseOperator):
    pass


# Will show up under airflow.sensors.test_plugin.PluginSensorOperator
class PluginSensorOperator(BaseSensorOperator):
    pass


# Will show up under airflow.executors.test_plugin.PluginExecutor
class PluginExecutor(BaseExecutor):
    pass


# Will show up under airflow.macros.test_plugin.plugin_macro
def plugin_macro():
    pass


class DemultiplexPluginView(BaseView):
    """This creates a flask admin blueprint view (I think)
    It shows up as http://localhost:8080/admin/demultiplexpluginview/
    I don't know why the def is test instead of init or something normal
    """
    @expose('/')
    def test(self):
        # in this example, put your test_plugin/test.html template at airflow/plugins/templates/test_plugin/test.html
        return self.render("test_plugin/test.html", content="Hello galaxy!")


v = DemultiplexPluginView(category="Demultiplex Plugin", name="Demultiplex Plugin")

# Creating a flask blueprint to integrate the templates and static folder
bp = Blueprint(
    "demultiplex_plugin", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/test_plugin')

ml = MenuLink(
    category='Demultiplex Plugin',
    name='Demultiplex Menu Link',
    url='https://airflow.incubator.apache.org/')


# Defining the plugin class
class AirflowDemultiplexPlugin(AirflowPlugin):
    name = "test_view_plugin"
    operators = [PluginOperator]
    sensors = [PluginSensorOperator]
    hooks = [PluginHook]
    executors = [PluginExecutor]
    macros = [plugin_macro]
    admin_views = [v]
    flask_blueprints = [bp]
    menu_links = [ml]

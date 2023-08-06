from typing import *
import click
from fifteenrock import core
from fifteenrock.core import compute_client
from fifteenrock.lib import util
import os
import json


@click.command()
@click.argument('command', required=True)
@click.option('--project', required=False, help='project name')
@click.option('--description', required=False, help='Description')
# @click.option('--function', required=False, help='function name')
@click.option('--url', required=False, help='url to 15Rock cluster')
@click.option('--main_file', type=click.Path(exists=True), required=False,
              help='path to file containing the main function')
@click.option('--dependencies', multiple=True, required=False,
              help='Files or folders to be placed in the same package at root of package')
@click.option('--requirements_file', type=click.Path(exists=True), required=False, help='Path to requirements.txt')
@click.option('--runtime', required=False, help='e.g. python')
@click.option('--runtime_version', required=False, help='e.g. 3.6')
@click.option('--project_folder', required=False, type=click.Path(exists=True),
              help='Path to the project root. This will also be the package root if specified')
@click.option('--credentials', multiple=True, required=False,
              help='key value pair of the format key=value. This will override --credentials_file')
@click.option('--credentials_file', type=click.Path(exists=True), required=False,
              help="Path to the credentials file. Either this or --credentials should be provided.")
@click.option('--config_file', type=click.Path(exists=True), required=False,
              help="JSON Path to configuration. The values will be overridden by values passed at the terminal. Note, that there won't be any merging of dicts.")
@click.option('--start_time', required=False,
              help='Start time of log entries. UTC Timestamp. %Y-%m-%dT%H:%M:%SZ. Refer to http://strftime.org/. e.g. 2019-06-13T13:52:00Z')
@click.option('--end_time', required=False,
              help='End time of log entries. UTC Timestamp %Y-%m-%dT%H:%M:%SZ. Refer to http://strftime.org/. e.g. 2019-06-13T13:52:01Z')
@click.option('--framework', required=False,
              help='One of flask or nuclio. default is nuclio')
def compute(command, project: str = None, description: str = None, url: str = None, main_file: str = None,
            dependencies: Tuple[str] = None, requirements_file: str = None, runtime: str = None, runtime_version: str
            = None, project_folder: str = None, credentials: Tuple[str] = None, credentials_file: str = None,
            config_file: str = None,
            start_time: str = None,
            end_time: str = None,
            framework: str = None):
    """Commands for the compute service"""
    # TODO: split credentials by key=value pair
    # TODO: Have a config file too where you can pass all the values?
    result = None
    dep_list = list(dependencies)
    credentials_list = list(credentials)
    credentials_dict = util.text_to_dict(credentials_list)
    fr_compute = compute_client.compute(url=url, credentials=credentials_dict, credentials_file=credentials_file)
    if command == 'deploy':
        # util.required('function', function)
        util.required('project', project)
        result = fr_compute.deploy(project, main_file=main_file, dependencies=dep_list,
                                   requirements_file=requirements_file, runtime=runtime,
                                   runtime_version=runtime_version, project_folder=project_folder,
                                   config_file=config_file,
                                   framework=framework,
                                   description=description)
        # result = core.deploy(project, function, url=url, main_file=main_file, dependencies=dep_list,
        #                      requirements_file=requirements_file,
        #                      runtime=runtime, runtime_version=runtime_version, project_folder=project_folder,
        #                      credentials=credentials_dict, credentials_file=credentials_file, config_file=config_file)

    elif command == 'list-projects':
        result = fr_compute.list_projects(project=project)

    elif command == 'delete-project':
        # util.required('function', function)
        util.required('project', project)
        result = fr_compute.delete_project(project=project)
    elif command == 'logs':
        # util.required('function', function)
        util.required('project', project)
        util.required('start_time', start_time)
        result = fr_compute.logs(project=project, start_time=start_time, end_time=end_time)
    print(json.dumps(result))

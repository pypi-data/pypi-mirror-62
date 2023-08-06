# -*- coding: utf-8 -*-

"""Main module."""
import json
import requests
from typing import *
from fifteenrock.lib import util, helper
from pyrsistent import freeze, pvector
import os
from shutil import copyfile
import pandas as pd
from pprint import pprint

PROJECT_NAME_ENV_KEY = 'FR_PROJECT_NAME'

DEFAULT_COMPUTE_ENDPOINT = 'https://app.15rock.com/gateway/compute'
REQUIREMENTS_FILE = 'requirements.txt'

ORG = 'default'
PORTFOLIO_MASTER_SUB = "/v1/master"
from json import JSONDecodeError


class BaseHandler(object):
    pass


def delete_project(project: str, url: str = None, credentials: Dict[str, str] = None,
                   credentials_file: str = None
                   ):
    # TODO: A lot of duplication with list_project etc.

    endpoint = 'project'
    raw_data = dict(project=project)

    endpoint_url = make_endpoint_url(url, endpoint)
    new_headers = make_headers(credentials, credentials_file)

    return util.delete(endpoint_url, raw_data=raw_data, headers=new_headers)


def make_headers(credentials, credentials_file):
    credentials = helper.get_credentials(credentials, credentials_file)
    headers = make_credentials_header(credentials)
    new_headers = {**headers, **{"Content-type": "application/json"}}
    return new_headers


def make_endpoint_url(url, endpoint):
    url = url or DEFAULT_COMPUTE_ENDPOINT
    endpoint_url = make_compute_url(url) + f'/{endpoint}'
    return endpoint_url


def logs(url: str = None, credentials: Dict[str, str] = None, credentials_file: str = None,
         project: str = None, start_time: str = None, end_time: str = None):
    endpoint = 'logs'
    raw_data = dict(project=project, start_time=start_time, end_time=end_time)
    endpoint_url = make_endpoint_url(url, endpoint)
    new_headers = make_headers(credentials, credentials_file)
    result = util.get_json(endpoint_url, raw_data=raw_data, headers=new_headers)
    if result['code'] == 200:
        return '\n'.join(result['result'])
    else:
        return result


def list_projects(url: str = None, credentials: Dict[str, str] = None, credentials_file: str = None,
                  project: str = None):
    filters = dict()
    if project:
        filters['project_name'] = project

    endpoint = 'project'
    raw_data = dict(filters=filters)

    credentials = helper.get_credentials(credentials, credentials_file)
    url = url or DEFAULT_COMPUTE_ENDPOINT
    list_url = make_compute_url(url) + f'/{endpoint}'
    headers = make_credentials_header(credentials)
    new_headers = {**headers, **{"Content-type": "application/json"}}

    response = util.get_response(list_url, raw_data=raw_data, headers=new_headers)

    if response:
        return response.json()
    else:
        return response.json()


def deploy(project: str, url: str = None, main_file: str = None, dependencies: List = None,
           requirements_file: str = None, runtime: str = None, runtime_version: str = None, project_folder: str = None,
           credentials: Dict[str, str] = None, credentials_file: str = None, spec: Dict = None, metadata: Dict = None,
           config_file: str = None,
           framework: str = None,
           main_module: str = None,
           description: str = None):
    """

    :param main_file:
    :param credentials:
    :param credentials_file: Path to the credentials file
    :param url:
    :param project:
    :param dependencies: files or folders not in your project_folder which you want to add to your deployment package.
        An example could be an external secrets file or some shared code outside your repo(which is not a pip
        library for e.g.)

    :param requirements_file:
    :param runtime:
    :param runtime_version:
    :param project_folder:
    :param spec: Dict of resources, image setup commands etc.
    :param metadata: Dict of labels, annotations etc.
    :param config_file: Config file. Any values passed in explicitly will override any values in the config file.
    Note, this pertains only to `spec` and `metadata` keys right now. i.e. if spec is provided, it will __completely__
    replace any values specified in the *config_file*
    :param framework: Currently supports one of ['nuclio', 'flask']
    :param main_module: For Nuclio style applications, the name of the main project. default 'main'. For Flask style
    applications, the name of the Flask instance(e.g. app = Flask(__name__), default 'app'.
    :return:
    """

    tmp_folder = util.tmp_folder()

    credentials = helper.get_credentials(credentials, credentials_file)
    config = helper.read_config(config_file)
    url = url or DEFAULT_COMPUTE_ENDPOINT
    main_file = main_file or helper.default_file_path('main.py')
    util.required('main_file', main_file)
    util.fail_if_no_file(main_file)
    if requirements_file:
        # copy_file with name requirements.txt

        dst = str(tmp_folder / REQUIREMENTS_FILE)
        copyfile(requirements_file, dst)
        requirements_file = dst
    else:
        requirements_file = helper.default_file_path(REQUIREMENTS_FILE) or str(util.make_requirements_file(tmp_folder))

    # project_folder = project_folder or os.getcwd()

    # requirements_file = requirements_file or str(util.make_requirements_file(tmp_folder))
    # name = name or util.file_name(main_file)
    dependencies = make_dependencies(dependencies, main_file, project_folder, requirements_file)

    spec = spec or config.get('spec') or dict()
    metadata = metadata or config.get('metadata') or dict()
    runtime = runtime or 'python'
    runtime_version = runtime_version or '3.6'

    runtime_path = tmp_folder / 'runtime.txt'
    runtime_path.write_text(runtime + '-' + runtime_version)
    credentials_tmp_path = tmp_folder / helper.FR_FILE_NAME

    dependencies = dependencies.append(str(runtime_path))

    util.write_credentials(credentials_tmp_path, credentials)

    dependencies = dependencies.append(str(credentials_tmp_path))
    # project_folder = project_folder or util.determine_project_folder()

    # dependencies = dependencies.extend([fifteenrock])

    # dependency_paths = [util.module_path(d) for d in dependencies]
    dependency_paths = pvector(str(util.module_path(d)) for d in dependencies)

    optional = util.optional(project=project, spec=spec, metadata=metadata, framework=framework,
                             main_module=main_module, description=description)
    mandatory = dict(credentials=credentials, main_file_name=os.path.basename(main_file))
    raw_data = {**mandatory, **optional}
    compute_url = make_compute_url(url)
    deploy_url = compute_url + '/deploy'

    archive_file = tmp_folder / 'archive.zip'

    from pathlib import Path
    util.archive(archive_file, dependency_paths)

    headers = make_credentials_header(credentials)
    try:
        deploy_result = deploy_to_compute(archive_file, headers, deploy_url, raw_data)

        if deploy_result['type'] == 'success':
            result = poll_if_project_created(deploy_result['project_id'], compute_url, headers)
        else:
            result = deploy_result
        import json
        if result['code'] == 400:
            detailed_message = json.loads(result.get('detailed_message', '{}'))
            if detailed_message:
                print(detailed_message['status']['message'])
            else:
                print(result)
        else:
            print(result)
        return result

    except Exception as e:
        raise e
    finally:
        util.remove_dir(tmp_folder)


def make_credentials_header(credentials):
    return dict(apikey=credentials['faas_token'])


def make_compute_url(url):
    compute_url = url + '/api/v0'
    return compute_url


def make_dependencies(dependencies, main_file, project_folder, requirements_file):
    dependencies = dependencies or []
    dependencies = freeze(dependencies)
    dependencies = dependencies.append(main_file)
    dependencies = dependencies.append(requirements_file)
    if project_folder:
        dependencies = dependencies.append(project_folder)
    return dependencies


# def poll_if_function_created(function_id, compute_url: str, headers: Dict):
#     tries = range(60)
#     interval = 30
#
#     import time
#
#     raw_data = dict(function_id=function_id)
#     status_url = compute_url + '/function_status'
#     new_headers = {**headers, **{"Content-type": "application/json"}}
#     for i in tries:
#         print(f'Try:{i}')
#         result = util.get_json(status_url, raw_data=raw_data, headers=new_headers)
#         code = result['code']
#         if code == 200:
#             return result
#         elif code == 40:
#             raise ValueError('Error in creating function')
#         # if code == 400:
#         #     # TODO: Report actual error
#         #     raise ValueError('Error in creating function')
#         # elif code == 200:
#         #     return result
#         time.sleep(interval)
#
#     # Else raise Timeout error
#     raise ValueError('Function creation timed out. Please try again.')

def poll_if_project_created(project_id, compute_url: str, headers: Dict):
    tries = range(60)
    interval = 30

    import time

    raw_data = dict(project_id=project_id)
    status_url = compute_url + '/project_status'
    new_headers = {**headers, **{"Content-type": "application/json"}}
    for i in tries:
        response = util.get_response(status_url, raw_data=raw_data, headers=new_headers)
        if response:
            result = response.json()
            code = result['code']
            if code == 200:
                return result
        else:
            error = response.json()
            return error

        time.sleep(interval)

    # Else raise Timeout error
    raise ValueError('Project creation timed out. Please try again.')


def deploy_to_compute(archive_file, headers, new_url, raw_data):
    return util.post(new_url, raw_data=raw_data, files={'archive': archive_file}, headers=headers)


# class DatabaseClient(object):
#     def __init__(self, url: str, credentials: Dict):
#         # self._url = url
#         self._url = url + '/' + 'v0'
#         self.credentials = credentials
#         pass
#
#     def url(self):
#         return self._url
#
#     # def drop(self, schema, table):
#     #     drop_query = f"DROP TABLE IF EXISTS {schema}.{table};"
#     #
#     #     self.execute_command(command=drop_query)
#
#     def query_sql(self, query: str):
#         raw_data = dict(credentials=self.credentials, query=query)
#         return self.post_json('/query_sql', raw_data)
#
#         # return result.json()
#
#     def post_json(self, url_part: str, raw_data: Dict):
#
#         headers = {"Content-type": "application/json"}
#
#         a_url = self.url() + url_part
#         try:
#             result = requests.post(a_url, headers=headers, data=json.dumps(raw_data))
#             js = result.json()
#             result.raise_for_status()
#             return js
#
#         except requests.exceptions.RequestException as e:
#             print(f"ROCK_ERROR:{json.dumps(js)}")
#             raise e
#
#     def execute_command(self, command: str):
#         result = self.post_json('/execute_command', dict(credentials=self.credentials, query=command))
#         # TODO: Start of GRAPHQL Code. Commenting for now
#         # tables = get_tables_to_track(query)
#         #
#         # for t in tables:
#         #
#         #     schema = t[0]
#         #     self.query_hasura([track_table(schema, t[1])])
#         #     table_info = self.query_hasura_single(get_table_info_for_relationships(schema))
#         #     if table_info:
#         #         fkc_dicts = get_foreign_key_constraints(table_info)
#         #         for fkc in fkc_dicts:
#         #             rel = get_object_relationship(fkc)
#         #             obj_rel_cmd = create_object_relationship(rel['label'], rel['schema'], rel['table_name'],
#         #                                                      rel['foreign_key'])
#         #             self.query_hasura_single(obj_rel_cmd)
#         #         for fkc in fkc_dicts:
#         #             rel = get_array_relationship(fkc)
#         #             arr_rel_cmd = create_array_relationship(rel['label'], rel['ref_schema'], rel['ref_table'],
#         #                                                     rel['schema'], rel['table_name'], rel['foreign_key'])
#         #             self.query_hasura_single(arr_rel_cmd)
#         # TODO: End of GRAPHQL Code. Commenting for now
#         return result
#
#     @staticmethod
#     def insert_query(table_name: str, columns: List, values: List):
#         cn = ', '.join(columns)
#         vn = []
#         for v in values:
#             if type(v) != str:
#                 vx = str(v)
#             else:
#                 vx = "'" + v + "'"
#             vn.append(vx)
#         vn = ', '.join(vn)
#         return f"INSERT INTO {table_name} ({cn}) VALUES ({vn});"
#
#     def insert_sql(self, table, columns, values):
#         inserts = [self.insert_query(table, columns, vn) for vn in values]
#         self.execute_command(command=''.join(inserts))
#
#     # def read(self, columns: List[str]):
#     #
#     #     return self.post_json('/read', dict(credentials=self.credentials, columns=json.dumps(columns)))
#
#     # def query_graphl(self, query: str):
#     #     request = requests.post(self.url() + "/graphql", json={'query': query})
#     #     if request.status_code == 200:
#     #         result = request.json()
#     #     else:
#     #         raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
#     #
#     #     return result
#
#     # def query_graphl(self, query: str):
#     #     return self.post_json('/graphql', dict(query=query))
#     #
#     # def query_hasura(self, query_dict: List[Dict]):
#     #     result = []
#     #     for q in query_dict:
#     #         r = self.post_json('/hasura_api', dict(query=q))
#     #         result.append(r)
#     #     return result
#     #
#     # def query_hasura_single(self, query_dict: Dict):
#     #     return self.post_json('/hasura_api', dict(query=query_dict))
#


class DatabaseClient(object):
    def __init__(self, url: str, credentials: Dict, project_name: str):
        # self._url = url
        # self._url = url + '/' + 'v0'
        # self._url = url + "/v1/project/default"
        self._url = url + "/v1/project/default"
        self.credentials = credentials
        self.project_name = project_name
        pass

    def url(self):
        return self._url

    # def drop(self, schema, table):
    #     drop_query = f"DROP TABLE IF EXISTS {schema}.{table};"
    #
    #     self.execute_command(command=drop_query)

    def query_sql(self, query: str, params: Dict = None):
        raw_data = query_raw_data(params, query, self.project_name)
        return self.post_json('/query_sql', raw_data)

        # return result.json()

    # def post_json(self, url_part: str, raw_data: Dict):
    #     headers = {"Content-type": "application/json",
    #                "apikey": self.credentials['faas_token']}
    #
    #     a_url = self.url() + url_part
    #     try:
    #
    #         result = requests.post(a_url, headers=headers, data=json.dumps(raw_data))
    #
    #         js = result.json()
    #         result.raise_for_status()
    #         # js = util.post(a_url, raw_data=raw_data, headers=headers)
    #         return js
    #
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error:{json.dumps(js)}")
    #         raise e

    def post_json(self, url_part: str, raw_data: Dict):
        result = None
        headers = {"Content-type": "application/json",
                   "apikey": self.credentials['faas_token']}

        a_url = self.url() + url_part
        try:

            result = requests.post(a_url, headers=headers, data=json.dumps(raw_data))

            result.raise_for_status()
            js = result.json()

            # js = util.post(a_url, raw_data=raw_data, headers=headers)
            return js

        except requests.exceptions.RequestException as e:
            if hasattr(result, 'json'):
                try:
                    payload = result.json()
                    if kong_authentication_error(payload):
                        raise ValueError('The `faas_token` is invalid. Please check your configuration file.')
                    return payload
                except JSONDecodeError as json_error:
                    raise e
                    pass

    def execute_command(self, command: str, params: Dict = None):
        raw_data = query_raw_data(params, command, self.project_name)
        result = self.post_json('/execute_command', raw_data)
        # TODO: Start of GRAPHQL Code. Commenting for now
        # tables = get_tables_to_track(query)
        #
        # for t in tables:
        #
        #     schema = t[0]
        #     self.query_hasura([track_table(schema, t[1])])
        #     table_info = self.query_hasura_single(get_table_info_for_relationships(schema))
        #     if table_info:
        #         fkc_dicts = get_foreign_key_constraints(table_info)
        #         for fkc in fkc_dicts:
        #             rel = get_object_relationship(fkc)
        #             obj_rel_cmd = create_object_relationship(rel['label'], rel['schema'], rel['table_name'],
        #                                                      rel['foreign_key'])
        #             self.query_hasura_single(obj_rel_cmd)
        #         for fkc in fkc_dicts:
        #             rel = get_array_relationship(fkc)
        #             arr_rel_cmd = create_array_relationship(rel['label'], rel['ref_schema'], rel['ref_table'],
        #                                                     rel['schema'], rel['table_name'], rel['foreign_key'])
        #             self.query_hasura_single(arr_rel_cmd)
        # TODO: End of GRAPHQL Code. Commenting for now
        return result

    @staticmethod
    def insert_query(table_name: str, columns: List, values: List):
        cn = ', '.join(columns)
        vn = []
        for v in values:
            if type(v) != str:
                vx = str(v)
            else:
                vx = "'" + v + "'"
            vn.append(vx)
        vn = ', '.join(vn)
        return f"INSERT INTO {table_name} ({cn}) VALUES ({vn});"

    def insert_sql(self, table, columns, values):
        inserts = [self.insert_query(table, columns, vn) for vn in values]
        self.execute_command(command=''.join(inserts))

    # def read(self, columns: List[str]):
    #
    #     return self.post_json('/read', dict(credentials=self.credentials, columns=json.dumps(columns)))

    # def query_graphl(self, query: str):
    #     request = requests.post(self.url() + "/graphql", json={'query': query})
    #     if request.status_code == 200:
    #         result = request.json()
    #     else:
    #         raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    #
    #     return result

    # def query_graphl(self, query: str):
    #     return self.post_json('/graphql', dict(query=query))
    #
    # def query_hasura(self, query_dict: List[Dict]):
    #     result = []
    #     for q in query_dict:
    #         r = self.post_json('/hasura_api', dict(query=q))
    #         result.append(r)
    #     return result
    #
    # def query_hasura_single(self, query_dict: Dict):
    #     return self.post_json('/hasura_api', dict(query=query_dict))


def query_raw_data(params, query, project_name):
    mandatory = dict(query=query, project_name=project_name)
    opt = util.optional(params=params)
    raw_data = {**mandatory, **opt}
    return raw_data


def database(url: str = "https://app.15rock.com/gateway/data",
             project_name: str = None,
             credentials: Dict = None,
             credentials_file: str = None) -> DatabaseClient:
    credentials = credentials or helper.get_credentials(credentials, credentials_file)
    project_name = project_name or os.environ.get(PROJECT_NAME_ENV_KEY)
    if not project_name:
        raise ValueError(
            f'project_name should be provided or set using import os, os.environ["{PROJECT_NAME_ENV_KEY}"] = <some_project_name>')
    return DatabaseClient(url, credentials, project_name)


def load_project(project_name: str,
                 table_name: str = None,
                 credentials: Dict = None,
                 credentials_file: str = None) -> pd.DataFrame:
    table_name = table_name or project_name

    query = "SELECT * from " + table_name

    credentials_json = helper.get_credentials(credentials, credentials_file)
    database_url = credentials_json.get('database_url')

    a_project_db = database(url=database_url, project_name=project_name)
    result = a_project_db.query_sql(query)
    result_df = pd.DataFrame.from_dict(result)

    return result_df


def deploy_powerBI(data: Dict, target: str):
    headers = {'Content-Type': 'application/json'}
    result = requests.post(target, headers, data)

    return result


def get_master_data_portfolio_url(
    entity_url: str,
    namespace: str,
    entity: str,
    filter_in: str = None,
    return_: str = None,
    return_except: str = None):
    entity_url_local = entity_url + f'/{ORG}/' + namespace + '/' + entity

    param_available = False

    if (filter_in or return_ or return_except):
        param_available = True

    if (param_available):
        entity_url_local += f'?a=a'

        if (filter_in):
            entity_url_local += f'&where={filter_in}'

        if (return_):
            entity_url_local += f'&return={return_}'

        if (return_except):
            entity_url_local += f'&return_except={return_except}'

    return entity_url_local


def get_master_data(namespace: str,
                    entity: str,
                    filter_in: str = None,
                    return_: str = None,
                    return_except: str = None,
                    credentials=None,
                    credentials_file=None,
                    ) -> pd.DataFrame:
    """
        sample url: https://staging.app.15rock.com/gateway/data/v1/master
    """

    # get the url from the json
    credentials_json = helper.get_credentials(credentials, credentials_file)

    if ('database_url' not in credentials_json):
        raise ValueError('Error in getting the database url from the credentials json')

    database_url = credentials_json['database_url']
    entity_url = database_url + PORTFOLIO_MASTER_SUB

    # getting the token
    if ('faas_token' not in credentials_json):
        raise ValueError('Error in getting the fass token from the credentials json')

    token = credentials_json['faas_token']
    headers = {"Content-type": "application/json", "apikey": token}

    entity_url_local = get_master_data_portfolio_url(entity_url, namespace,
                                                     entity, filter_in, return_, return_except)

    result = requests.get(entity_url_local, headers=headers).json()

    entity_df = pd.DataFrame(result['result'])

    return entity_df


def ludwig_features_detection(dataframe, output_name):
    columns = list(dataframe.columns)
    dtypes = []
    for c in columns:
        dtypes.append(dataframe[c].dtype)

    dtypes2 = []
    for d in dtypes:
        if d in ('int64', 'float64'):
            dtypes2.append('numerical')
        if d == object:
            dtypes2.append('category')

    input_features = []
    output_feature = []
    for col, dtype in zip(columns[:-1], dtypes2[:-1]):
        # print(col, dtype)
        if col == output_name:
            output_feature.append(dict(name=col, type=dtype))
        else:
            input_features.append(dict(name=col, type=dtype))

    # print(input_features)
    # print(output_feature)
    return input_features, output_feature


def kong_authentication_error(payload: Dict) -> bool:
    message = payload.get('message')
    if message == "Invalid authentication credentials":
        return True
    else:
        return False
    pass


def model_train(dataframe, output_field):
    from ludwig.api import LudwigModel
    import ludwig
    input_features, output_feature = ludwig_features_detection(dataframe, output_field)
    model_definition = {'input_features': input_features, 'output_features': output_feature}

    model = LudwigModel(model_definition)
    trainstats = model.train(dataframe)

    print(trainstats)
    print("Thank you for using 15Rock's AutoTraining, Training is complete.")
    return model


# model = model_train(total_view, 'gender')

# model = fifteenrock.model_train(DATAFRAME, column)


# predictions = model.predict(new_total_view)


# def is_create_cmd(stmt):
#     return stmt.get_type() == 'CREATE'
#     pass


# def flatten(ll):
#     return [lu for l in ll for lu in l]

#
# def is_create_table_stmt(s):
#     # return s.get_type() == 'CREATE' and s.parent.get_type()
#     return 'create table' in s.value.lower()


# def get_tables_to_track(ddl):
#     parsed = sqlparse.parse(ddl)
#     create_stmts = list(filter(is_create_table_stmt, parsed))
#     all_tokens = flatten(map(lambda s: s.tokens, create_stmts))
#
#     table_tokens = list(filter(lambda t: t._get_repr_name() == 'Identifier', all_tokens))
#     #
#     return list(map(lambda tt: (tt.get_parent_name(), tt.get_name()), table_tokens))
#     pass


# def get_query(columns: List[str], meta, engine):
#     splits = [c.split('.') for c in columns]
#
#     full_columns = []
#     for s in splits:
#         if len(s) == 2:
#             schema_name = "public"
#             table_name = s[0]
#             column_name = s[1]
#         else:
#             schema_name = s[0]
#             table_name = s[1]
#             column_name = s[2]
#         full_columns.append(FullColumn(schema_name, table_name, column_name))
#
#     full_tables = []
#     for s in splits:
#         if len(s) == 2:
#             schema_name = "public"
#             table_name = s[0]
#         else:
#             schema_name = s[0]
#             table_name = s[1]
#         full_tables.append(FullTable(schema_name, table_name))
#
#     new_tables = inner_join_strs(set(full_tables), meta, engine)
#     fc_strs = ['.'.join([fc.schema_name, fc.table_name, fc.column_name]) for fc in full_columns]
#     new_columns = ', '.join(fc_strs)
#
#     query = f'''SELECT {new_columns} from {new_tables};'''
#
#     return query
#
#
# def get(user: str, columns: List[str]):
#     meta = MetaData()
#     q = get_query(columns, meta, db)
#     return read_sql(user, q)
#     pass


#
#
# def select_str(column_strs):
#     column_str = ', '.join(column_strs)
#     return f'''
# SELECT {column_str}
# '''
#
#
# def inner_join_str(pk_schema: str, pk_table: str, pk: str, fk_schema: str, fk_table: str, fk: str):
#     pk_table_full = f"{pk_schema}.{pk_table}"
#     fk_table_full = f"{fk_schema}.{fk_table}"
#     return f'''
# {pk_table_full} INNER JOIN {fk_table_full}
# ON {pk_table_full}.{pk} = {fk_table_full}.{fk}
# '''
#
#
# def to_alchemy_tables(tables: List[FullTable], meta, engine):
#     return [Table(t.table_name, meta, autoload=True, autoload_with=engine, schema=t.schema_name) for t in tables]
#
#
# def get_foreign_keys(alchemy_table):
#     return list(alchemy_table.foreign_keys)
#
#
# # pprint(inner_join_str(fk.column.table.schema, fk.column.table.name, fk.column.name, 'public', 'scoring_model',
# #                       fk.parent.name))
#
#
# def get_primary_full_table(fk):
#     return FullTable(fk.column.table.schema, fk.column.table.name)
#
#
# def exists(a_full_table, full_tables) -> bool:
#     for ft in full_tables:
#         if ft.schema_name == a_full_table.schema_name and ft.table_name == a_full_table.table_name:
#             return True
#     return False
#
#
# def inner_join_strs(full_tables, meta, engine):
#     final_joins = []
#     alchemy_tables = to_alchemy_tables(full_tables, meta, engine)
#     if len(full_tables) > 1:
#         for table in alchemy_tables:
#             fks = get_foreign_keys(table)
#             for fk in fks:
#                 pk_table = get_primary_full_table(fk)
#                 if exists(pk_table, full_tables):
#                     an_inner_join = inner_join_str(pk_table.schema_name, pk_table.table_name, fk.column.name,
#                                                    table.schema,
#                                                    table.name, fk.parent.name)
#                     final_joins.append(an_inner_join)
#         return final_joins[0]
#     else:
#         full_table = list(full_tables)[0]
#         return full_table.schema_name + '.' + full_table.table_name
#
#
# def query_graphl(query: str):
#     request = requests.post("http://localhost:8080/v1alpha1/graphql", json={'query': query})
#     if request.status_code == 200:
#         result = request.json()
#     else:
#         raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
#
#     return result
#
#


if __name__ == '__main__':
    #     db_string = "postgres://postgres:@localhost:5432/postgres"
    #     # engine = create_engine(db_string)
    #     # meta = MetaData()
    #     assert get_query(columns=['public.customer.name']) == 'SELECT public.customer.name from public.customer;'
    #     assert get_query(columns=['public.customer.name',
    #                               'public.customer.age']) == 'SELECT public.customer.name, public.customer.age from public.customer;'
    #
    #     first_join_query = """SELECT public.customer.name, public.scoring_model.score from
    # public.customer INNER JOIN public.scoring_model
    # ON public.customer.id = public.scoring_model.customer_id
    # ;"""
    #     assert get_query(columns=["public.customer.name", "public.scoring_model.score"]) == first_join_query
    #     assert get_query(columns=["customer.name", "scoring_model.score"]) == first_join_query
    #     tables = [FullTable("public", "customer"),
    #               FullTable("public", "scoring_model")]
    #     final_join = inner_join_strs(tables)
    #
    #     exp_join = '''
    # public.customer INNER JOIN public.scoring_model
    # ON public.customer.id = public.scoring_model.customer_id
    # '''
    #     assert final_join == exp_join

    # def drop_relationship(schema, table, relationship):
    #     return {
    #         "type": "drop_relationship",
    #         "args": {
    #             "table": dict(schema=schema, name=table),
    #             "relationship": relationship
    #         }
    #     }

    # def untrack_table(schema, table):
    #     return {
    #         "type": "untrack_table",
    #         "args": {
    #             "table": {
    #                 "schema": schema,
    #                 "name": table
    #             },
    #             "cascade": True
    #         }
    #     }
    #

    # def track_table(schema, table):
    #     return {
    #         "type": "track_table",
    #         "args": {
    #             "schema": schema,
    #             "name": table
    #         }
    #     }

    # def create_array_relationship(relationship_name, schema, table, foreign_schema, foreign_table, foreign_column):
    #     # return {"type": "create_array_relationship", "args": {"name": "scoringModelsBycustomerId",
    #     #                                                       "table": {"name": "customer",
    #     #                                                                 "schema": "demo"},
    #     #                                                       "using": {
    #     #                                                           "foreign_key_constraint_on": {
    #     #                                                               "table": {
    #     #                                                                   "name": "scoring_model",
    #     #                                                                   "schema": "demo"},
    #     #                                                               "column": "customer_id"}}}}
    #
    #     return {"type": "create_array_relationship", "args": {"name": relationship_name,
    #                                                           "table": {"name": table,
    #                                                                     "schema": schema},
    #                                                           "using": {
    #                                                               "foreign_key_constraint_on": {
    #                                                                   "table": {
    #                                                                       "name": foreign_table,
    #                                                                       "schema": foreign_schema},
    #                                                                   "column": foreign_column}}}}
    #

    # create_array_relationship("scoringModelsBycustomerId", "demo", 'customer', 'demo', 'scoring_model', 'customer_id')

    # def create_object_relationship(relationship_name, schema, table, foreign_column):
    #     return {"type": "create_object_relationship", "args": {"name": relationship_name,
    #                                                            "table": {"name": table,
    #                                                                      "schema": schema}, "using": {
    #             "foreign_key_constraint_on": foreign_column}}}

    # create_object_relationship("customerBycustomerId", 'demo', 'scoring_model', 'customer_id')

    # def drop_table(schema, table):
    #     return {"type": "run_sql", "args": {"sql": f"DROP TABLE {schema}.{table}"}}

    # def get_object_relationship(constraint):
    #     fk = list(constraint['column_mapping'].keys())[0]
    #     label = constraint['ref_table'] + 'By' + fk
    #     return dict(label=label, schema=constraint['table_schema'], table_name=constraint['table_name'], foreign_key=fk)

    # def get_array_relationship(constraint):
    #     c = constraint
    #     table_name = c['table_name']
    #     fk = list(c['column_mapping'].keys())[0]
    #     label = table_name + 's' + 'By' + fk
    #     return dict(label=label, ref_schema=c['ref_table_table_schema'], ref_table=c['ref_table'], schema=c['table_schema'],
    #                 table_name=table_name, foreign_key=fk)
    #

    # def get_foreign_key_constraints(mappings):
    #     fkc_dicts = flatten([m['foreign_key_constraints'] for m in mappings if
    #                          'foreign_key_constraints' in m and m['foreign_key_constraints']])
    #     return fkc_dicts
    #
    #
    # def get_table_info_for_relationships(schema):
    #     return {"type": "select", "args": {"table": {"name": "hdb_table", "schema": "hdb_catalog"}, "columns": ["*.*",
    #                                                                                                             {
    #                                                                                                                 "name": "columns",
    #                                                                                                                 "columns": [
    #                                                                                                                     "*.*"],
    #                                                                                                                 "order_by": [
    #                                                                                                                     {
    #                                                                                                                         "column": "column_name",
    #                                                                                                                         "type": "asc",
    #                                                                                                                         "nulls": "last"}]}],
    #                                        "where": {"table_schema": schema},
    #                                        "order_by": [{"column": "table_name", "type": "asc", "nulls": "last"}]}}
    #
    # url = 'http://localhost:8082'

    # print(os.path.basename(main_path))
    # print(os.path.splitext(os.path.basename(main_path))[0])

    pass

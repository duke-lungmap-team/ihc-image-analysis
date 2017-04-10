import os
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from lungmap_sparql_client.lungmap_sparql_queries import *
import warnings
from dateutil import parser
import boto3

lm_mother_ship = "http://testdata.lungmap.net/sparql"


def list_all_lungmap_experiments():
    """
    Call out to the LM mothership (via SPARQL) to get a list of all experiements that have an image. NOTE: this could
    mean a .tif image or .png image (or something else). No restriction is placed on the type of image.
    :return: status of sparql query
    """
    try:
        sparql = SPARQLWrapper(lm_mother_ship)
        sparql.setQuery(ALL_EXPERIMENTS_WITH_IMAGE)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        output = []
        for x in results['results']['bindings']:
            output.append(x['experiment']['value'].split('#')[1])
        return output
    except ValueError as e:
        raise e


def _get_by_experiment(query, experiment_id):
    """
    Query LM mothership (via SPARQL) and get information by a given experiment_id for a particular experiment
    :param query_name: a predefined query string from lungmap_sparql_client that has the replacement 
    string EXPERIMENT_PLACEHOLDER
    :param experiment_id: valid experiment_id from lungmap
    :return:
    """
    try:
        query_sub = query.replace('EXPERIMENT_PLACEHOLDER', experiment_id)
        sparql = SPARQLWrapper(lm_mother_ship)
        sparql.setQuery(query_sub)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings']
    except ValueError as e:
        raise e


def get_experiment_model_data(experiment_id):
    """
    Combines three lungmap_sparql_utils functions to provide data to the Experiment model via dict
    :param experiment_id: str: lungmap id
    :return: dict that matches the columns in the Experiment model
    """
    types = get_experiment_type_by_experiment(experiment_id)
    # researcher = get_researcher_by_experiment(experiment_id)
    sample = get_sample_by_experiment(experiment_id)
    # result = {**types, **researcher, **sample, **{"experiment_id": experiment_id}}
    result = {**types, **sample, **{"experiment_id": experiment_id}}
    return result


def get_sample_by_experiment(experiment_id):
    results = _get_by_experiment(GET_SAMPLE_BY_EXPERIMENT , experiment_id)
    if (len(results)>1):
        warnings.warn('get_sample_by_experiment: more than 1 sample received, only passing the first result.')
    try:
        for x in results[:1]:
            row = {}
            row['age_label'] = x['age_label']['value']
            row['sex'] = x['sex']['value'].lower()
            row['organism_label'] = x['organism_label']['value']
            row['local_id'] = x['local_id']['value']
        return row
    except ValueError as e:
        raise e


def get_images_by_experiment(experiment_id):
    results = _get_by_experiment(GET_IMAGES_BY_EXPERIMENT,experiment_id)
    output = []
    try:
        for x in results:
            row = {}
            filename = x['img_file']['value']
            name, ext = os.path.splitext(filename)
            root = x['experiment']['value'].split('owl#')[1]
            s3_obj_key = os.path.join(root, name, filename)
            row['file_ext'] = ext
            row['image_name'] = filename
            row['image_id'] = x['image']['value'].split('owl#')[1]
            row['s3key'] = s3_obj_key
            row['experiment_id'] = root
            row['magnification'] = x['magnification']['value']
            row['x_scaling'] = x['x_scaling']['value']
            row['y_scaling'] = x['y_scaling']['value']
            output.append(row)
        return output
    except ValueError as e:
        raise e


def get_probes_by_experiment(experiment_id):
    results = _get_by_experiment(GET_PROBE_BY_EXPERIMENT,experiment_id)
    output = []
    try:
        for x in results:
            row = {}
            row['color'] = x['color']['value']
            row['probe_label'] = x['probe_label']['value']
            output.append(row)
        return output
    except ValueError as e:
        raise e


def get_experiment_type_by_experiment(experiment_id):
    results = _get_by_experiment(GET_EXPERIMENT_TYPE_BY_EXPERIMENT, experiment_id)
    if (len(results)>1):
        raise ValueError('lungmap_sparql_client.lungmap_sparql_utils.get_experiment_type_by_experiment error too many results.')
    try:
        for x in results:
            row = {}
            row['platform'] = x['platform']['value']
            row['release_date'] = parser.parse(x['release_date']['value']).strftime('%Y-%m-%d')
            row['experiment_type_label'] = x['experiment_type_label']['value']
        return row
    except ValueError as e:
        raise e


def get_researcher_by_experiment(experiment_id):
    results = _get_by_experiment(GET_RESEARCHER_BY_EXPERIMENT, experiment_id)
    if (len(results)>1):
        raise ValueError('lungmap_sparql_client.lungmap_sparql_utils.get_experiment_type_by_experiment error too many results.')
    try:
        for x in results:
            row = {}
            row['researcher_label'] = x['researcher_label']['value']
            row['site_label'] = x['site_label']['value']
        return row
    except ValueError as e:
        raise e





import os
from SPARQLWrapper import SPARQLWrapper, JSON
from lungmap_sparql_client.lungmap_sparql_queries import *
import boto3


def _query_lungmap_experiment(query_name, experiment_id):
    """
    Internal function that queries lungmap based on set query (query_name) and experiment_id
    :param query_name: str from lungmap_sparql_client.lungmap_sparql_queries
    :param experiment_id: valid experiment_id from lungmap
    :return:
    """
    query_sub = query_name.replace('EXPERIMENT_PLACEHOLDER', experiment_id)
    sparql = SPARQLWrapper("http://testdata.lungmap.net/sparql")
    sparql.setQuery(query_sub)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def get_lungmap_file_list():
    """
    This function queries the lungmap sparql resource to obtain a list of dicts that contains all files with extension
    '.tif' or '.tiff'.
    :return: comprehensive list of dictionaries detailing all tif images and associated metadata.
    """
    sparql = SPARQLWrapper("http://testdata.lungmap.net/sparql")
    sparql.setQuery(ALL_EXPERIMENTS)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    index = []
    for i, x in enumerate(results['results']['bindings']):
        filename = x.get('raw_file').get('value')
        name, ext = os.path.splitext(filename)
        if ext == '.tif' or ext == '.tiff':
            index.append(i)
    tif_files = [results['results']['bindings'][i] for i in index]
    return tif_files

def get_lungmap_file_list_all():
    """
    This function queries the lungmap sparql resource to obtain a list of dicts that contains all files regarless of their
    extension
    :return: comprehensive list of dictionaries detailing all tif images and associated metadata.
    """
    sparql = SPARQLWrapper("http://testdata.lungmap.net/sparql")
    sparql.setQuery(ALL_EXPERIMENTS)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']

def download_s3_lungmap_image(lungmap_file_dictionary, location):
    """
    Takes a dictionary object (only 1) from the
    lungmap_sparql_client.lungmap_sparql_client.get_lungmap_file_list function
    and downloads the image to a location specified
    :param lungmap_file_dictionary: dict
    :param location: str, UNC path where file should be stored
    :return:
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('lungmap-breath-data')
    filename = lungmap_file_dictionary.get('raw_file').get('value')
    name, ext = os.path.splitext(filename)
    root = os.path.basename(os.path.normpath(lungmap_file_dictionary.get('path').get('value')))
    s3objkey = os.path.join(root, name, filename)
    filepath = os.path.join(location, root, name)
    if not os.path.exists(filepath):
        print("Creating directory: ", filepath)
        os.makedirs(filepath)
    if not os.path.isfile(os.path.join(filepath, filename)):
        print("Downloading file: ", filename)
        bucket.download_file(s3objkey, os.path.join(filepath, filename))


def get_experiment_researchers_and_sites(experiment_id):
    """
    Submit an experiment_id (e.g. LMEX000000000X) and in return a dictionary of metadata about that experiment is
    generated which includes the following keys: distinct, bindings (list of dicts), ordered
    :param experiment_id: str
    :return: dictionary of metadata about a particular experiment
    """
    results = _query_lungmap_experiment(RESEARCHERS_AND_SITES, experiment_id)
    return results['results']


def get_experiment_description_platform(experiment_id):
    """
    Submit an experiment_id (e.g. LMEX000000000X) and in return a dictionary of metadata about that experiment is
    generated which includes the following keys: bindings(list of dicts), ordered, distinct
    :param experiment_id: str
    :return: dictionary of metadata about a particular experiment
    """
    results = _query_lungmap_experiment(DESCRIPTION_AND_PLATFORM, experiment_id)
    return results['results']


def get_experiment_probe_antibody_strain(experiment_id):
    """
    Submit an experiment_id (e.g. LMEX000000000X) and in return a dictionary of metadata about that experiment is
    generated which includes the following keys: bindings (list of dicts), ordered, distinct
    :param experiment_id: str
    :return: dictionary of metadata about a particular experiment
    """
    results = _query_lungmap_experiment(PROBE_STAIN, experiment_id)
    return results['results']


def get_experiment_sample_details(experiment_id):
    """
    Submit an experiment_id (e.g. LMEX000000000X) and in return a dictionary of metadata about that experiment is
    generated which includes the following keys: bindings (list of dicts), ordered, distinct
    :param experiment_id: str
    :return: dictionary of metadata about a particular experiment
    """
    results = _query_lungmap_experiment(SAMPLE_DETAILS, experiment_id)
    return results['results']


def get_experiment_anatomy(experiment_id):
    """
    Submit an experiment_id (e.g. LMEX000000000X) and in return a dictionary of metadata about that experiment is
    generated which includes the following keys: bindings (list of dicts), ordered, distinct
    :param experiment_id: str
    :return: dictionary of metadata about a particular experiment
    """
    results = _query_lungmap_experiment(EXPERIMENT_ANATOMY, experiment_id)
    return results['results']


def get_experiment_images(experiment_id):
    """
    Submit an experiment_id (e.g. LMEX000000000X) and in return a dictionary of metadata about that experiment is
    generated which includes the following keys: bindings (list of dicts), ordered, distinct
    :param experiment_id: str
    :return: dictionary of metadata about a particular experiment
    """
    results = _query_lungmap_experiment(EXPERIMENT_IMAGES, experiment_id)
    return results['results']

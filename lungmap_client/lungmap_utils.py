from lungmap_client import lungmap_sparql_queries as sparql_queries
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import requests
import tempfile
import gzip


lungmap_sparql_server = "http://data.lungmap.net/sparql"


def get_image_set_candidates():
    sparql = SPARQLWrapper(lungmap_sparql_server)
    sparql.setQuery(sparql_queries.GET_BASIC_EXPERIMENTS)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    experiments = {}
    for r in results['results']['bindings']:
        e_id = r['experiment_id']['value'].split('#')[1]

        if e_id in experiments.keys():
            # looks like there are some experiments with multiple development stage strings
            print('Duplicate experiment %s' % e_id)
            print(
                'Species: %s vs %s, DevStage: %s vs %s' % (
                    experiments[e_id]['species'],
                    r['species']['value'],
                    experiments[e_id]['development_stage'],
                    r['stage_label']['value']
                )
            )

        experiments[e_id] = {
            'species': r['species']['value'],
            'development_stage': r['stage_label']['value']
        }

    images = []

    for e_id, e in experiments.items():
        e_probes = get_probes_by_experiment(experiment_id=e_id)

        # very important to sort probes by probe label to make sure the string is consistent
        # in order to combine images from experiments with the same probe / color combos
        e['probes'] = sorted(e_probes, key=lambda k: k['probe_label'])

        e_images = get_images_by_experiment(e_id)
        images.extend(e_images)

    image_sets = {}

    for i in images:
        e = experiments[i['experiment_id']]

        species = e['species']
        dev_stage = e['development_stage']
        probes = e['probes']
        magnification = i['magnification']
        probe_combo_str = "_".join(
            ["__".join([p['probe_label'], p['color']]) for p in e['probes']])

        i_set_str = "_".join([species, dev_stage, magnification, probe_combo_str])

        if i_set_str in image_sets.keys():
            image_sets[i_set_str]['images'].append({
                "image_id": i['image_id'],
                "image_name": i['image_name'],
                "x_scaling": i['x_scaling'],
                "y_scaling": i['y_scaling'],
                "source_url": i["source_url"],
                "experiment_id": i["experiment_id"],
                "experiment_type_id": i["experiment_type_id"]
            })
        else:
            image_sets[i_set_str] = {
                'species': species,
                'development_stage': dev_stage,
                'probes': probes,
                'experiments': [],
                'magnification': magnification,
                'images': [{
                    "image_id": i['image_id'],
                    "image_name": i['image_name'],
                    "x_scaling": i['x_scaling'],
                    "y_scaling": i['y_scaling'],
                    "source_url": i["source_url"],
                    "experiment_id": i["experiment_id"],
                    "experiment_type_id": i["experiment_type_id"]
                }]
            }
    for key, value in image_sets.items():
        for x in value['images']:
            if x['image_id'].split('_')[0] not in image_sets[key]['experiments']:
                image_sets[key]['experiments'].append(
                    {
                        'experiment_id': x['experiment_id'],
                        'experiment_type_id': x['experiment_type_id']
                    }
                )

    return image_sets


def _get_by_experiment(query, experiment_id):
    """
    Query LM mothership (via SPARQL) and get information by a given 
    experiment_id for a particular experiment
    :param query: a predefined query string from lungmap_client that 
    has the replacement string EXPERIMENT_PLACEHOLDER
    :param experiment_id: valid experiment_id from lungmap
    :return:
    """
    try:
        query_sub = query.replace('EXPERIMENT_PLACEHOLDER', experiment_id)
        sparql = SPARQLWrapper(lungmap_sparql_server)
        sparql.setQuery(query_sub)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings']
    except ValueError as e:
        raise e


def get_images_by_experiment(experiment_id):
    results = _get_by_experiment(
        sparql_queries.GET_IMAGES_BY_EXPERIMENT,
        experiment_id
    )
    output = []
    try:
        for x in results:
            row = {
                'image_name': os.path.basename(x['image_file_path']['value']).rsplit('.', 1)[0],
                'image_id': x['dir']['value'], 'source_url': x['image_file_path']['value'],
                'experiment_id': experiment_id,
                'experiment_type_id': x['experiment_type']['value'],
                'magnification': x['magnification']['value'],
                'x_scaling': x['x_scaling']['value'], 'y_scaling': x['y_scaling']['value']
            }

            output.append(row)
        return output
    except ValueError as e:
        raise e


def get_probes_by_experiment(experiment_id):
    results = _get_by_experiment(
        sparql_queries.GET_PROBE_BY_EXPERIMENT,
        experiment_id
    )
    output = []
    try:
        for x in results:
            row = {
                'color': x['color']['value'],
                'probe_label': x['probe_label']['value']
            }
            output.append(row)
        return output
    except ValueError as e:
        raise e


def get_image_from_lungmap(url):
    """
    Takes a URL and downloads the image,
    returns file name and image data as file object
    :param url: source URL for the image resource
    :return: file name, TIFF data as bytes object
    """
    filename = url.split('/')[-1]
    base, ext = os.path.splitext(filename)  # this extension is just the .gz of .tiff.gz

    # TODO: check response, if not successful we cannot proceed
    response = requests.get(url, stream=True)

    with tempfile.NamedTemporaryFile(suffix=ext) as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

        f.seek(0)

        with gzip.GzipFile(mode='rb', fileobj=f) as f2:
            tiff_data = f2.read()

        f2.close()

    response.close()

    return base, tiff_data

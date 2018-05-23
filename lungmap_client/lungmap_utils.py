# noinspection PyPackageRequirements
import cv2
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from lungmap_client import lungmap_sparql_queries as sparql_queries
from SPARQLWrapper import SPARQLWrapper, JSON
import hashlib
import os
# noinspection PyPackageRequirements
from PIL import Image
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
    Takes a URL and downloads the image, calculates a SHA1,
    creates a SimpleUploadedFile, converts to jpeg
    and then creates another SimpleUploadedFile for the jpeg, 
    returns 3 objects
    :param url:
    :return: SimpleUploadedFile (orig), SHA1 Hash (orig), 
    SimpleUploadedFile (jpeg converted)
    """
    try:
        filename = url.split('/')[-1]
        base, ext = os.path.splitext(filename)

        # TODO: check response, if not successful we cannot proceed
        response = requests.get(url, stream=True)

        with tempfile.NamedTemporaryFile(suffix=ext) as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

            f.seek(0)

            with gzip.GzipFile(mode='rb', fileobj=f) as f2:
                tiff_data = f2.read()

            f2.close()

            with open(f.name[:-3], 'wb') as f3:
                f3.write(tiff_data)

                # noinspection PyUnresolvedReferences
                cv_img = cv2.imread(f3.name)

        response.close()
        os.remove(f3.name)

        # noinspection PyUnresolvedReferences
        img = Image.fromarray(
            cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB),
            'RGB'
        )
        img_jpeg = img.copy()
        temp_handle = BytesIO()
        img.save(temp_handle, 'TIFF')
        temp_handle.seek(0)

        # jpeg image
        temp_handle_jpeg = BytesIO()
        img_jpeg.save(temp_handle_jpeg, 'JPEG')
        temp_handle_jpeg.seek(0)

        # filename
        suf = SimpleUploadedFile(
            base,
            temp_handle.read(),
            content_type='image/tif'
        )
        suf_jpg = SimpleUploadedFile(
            base.replace('.tif', '.jpg'),
            temp_handle_jpeg.read(),
            content_type='image/jpeg'
        )

        temp_handle.seek(0)
        image_orig_sha1 = hashlib.sha1(temp_handle.read()).hexdigest()

        return suf, image_orig_sha1, suf_jpg
    except ValueError as e:
        raise e

from lungmap_sparql_client.lungmap_sparql_utils import *
from tqdm import tqdm
import pandas as pd
import json
import os
from dateutil import parser


class LMClient(object):
    def __init__(self):
        """
        initializes a LMClient that is tied to a particular location. This location is used to copy images from S3
        Lungmap to this location as well as save pandas dataframe representations of the metadata.
        """
        print("Generating Metadata for all '.tif' or '.tiff' images within lungmap")
        self.image_list = self.create_image_table(get_lungmap_file_list)
        print("Generating Metadata for all probes associated with '.tif' or '.tiff' images within lungmap")
        self._create_probe_list()
        print("Generating Metadata for all conditions associated with a probe")
        self._create_condition_list()

    @staticmethod
    def _get_media_inventory(media_location):
        """
        This is the only function in this package that ties it to django configurations because it will take
        the media_location provided and then append two folders (images, images_jpeg) to that location
        to then do a recursive search to find what files are available and already downloaded. This will be used to
        stand up a database in the case of starting over and not wanting to download all images again.
        :return: dict of two lists. two keys 'images' and 'images_jpeg'
        """
        output = []
        for dirname, dirnames, filenames in os.walk(media_location):
            filenames = [f for f in filenames if not f[0] == '.']
            endpoint_path = os.path.relpath(dirname, media_location)
            for filename in filenames:
                output.append(os.path.join(endpoint_path, filename))
        return output

    @classmethod
    def create_image_table(self, func):
        """
        Internal function used to generate an attribute that is a list of dicts where keys are varaibles in the
        analytics.image model.
        :return: assigns image_table attribute to self
        """
        tables = func()
        rows = []
        for x in tqdm(tables):
            output = {'image_id': x['image_id']['value'].split('owl#')[1]}
            filename = x.get('raw_file').get('value')
            name, ext = os.path.splitext(filename)
            root = os.path.basename(os.path.normpath(x.get('path').get('value')))
            s3_obj_key = os.path.join(root, name, filename)
            output['file_ext'] = ext
            output['image_name'] = filename
            output['s3key'] = s3_obj_key
            output['age'] = x['age_label']['value']
            output['experiment_id'] = x['experiment_id']['value'].split('owl#')[1]
            output['gender'] = x['gender']['value']
            output['magnification'] = x['magnification']['value']
            output['organism'] = x['organism_label']['value']
            output['strain'] = x['strain']['value']
            output['date'] = parser.parse(x['date']['value']).strftime('%Y-%m-%d')
            output['image_orig'] = ''
            output['image_orig_sha1'] = ''
            output['image_jpeg'] = ''
            rows.append(output)
        return rows

    def _create_probe_list(self):
        """
        Generate the probe table (i.e. self.probe_list)
        :return:
        """
        unique_ids = self.get_unique_keys('experiment_id')
        output = []
        for x in tqdm(unique_ids):
            probes = get_experiment_probe_antibody_strain(x)
            for z in probes['bindings']:
                results = {
                    'color': z['color']['value'],
                    'probe_id': z['probe_id']['value'].split('owl#')[1],
                    'probe_name': z['probe_label']['value'],
                    'target_conditions': z['target_conditions']['value'],
                    'target_molecules': z['target_molecules']['value'],
                    'experiment_id': z['experiment_id']['value'].split('owl#')[1]
                }
                output.append(results)
        self.probe_list = output

    def _create_condition_list(self):
        output = []
        for x in tqdm(self.probe_list):
            bar_split = x.get('target_conditions').split('|')
            for z in bar_split:
                row = {'probe_id': x.get('probe_id')}
                semi_split = z.split(';')
                row['condition'] = semi_split[1]
                output.append(row)
        self.condition_list = output

    def generate_repository_fixtures(self, location):
        """
        Generates all fixutres defined as part of the LMClient Class
        :return: None
        """
        if not os.path.exists(location):
            os.makedirs(location)
        print('Generating repository.image fixture (image.json)')
        self.create_image_fixture(location)
        print('Generating respository.experiment fixture (experiment.json)')
        self.create_experiment_fixture(location)
        # print('Generating respository.age fixture (age.json)')
        # self.create_age_fixture()
        # print('Generating repository.gender fixture (gender.json)')
        # self.create_gender_fixture()
        # print('Generating respository.magnification fixture (magnification.json)')
        # self.create_magnification_fixture()
        # print('Generating repository.organism fixture (organism.json)')
        # self.create_organism_fixture()
        # print('Generating repository.experimentprobe fixture (experimentprobe.json')
        # self.create_experimentprobe_fixture()
        # print('Generating repository.condition fixture (condition.json)')
        # self.create_condition_fixture()
        print('Generating repository.probe fixture (probe.json)')
        self.create_probe_fixture(location)

    def create_image_fixture(self, location):
        """
        Creates a fixture for the repository.image model (i.e. image.json)
        :return:
        """
        if not os.path.exists(location):
            os.makedirs(location)
        output = []
        for i, x in enumerate(self.image_list):
            output.append({"model": "analytics.lungmapimage",
                           "pk": i + 1,
                           "fields": x})
        with open(os.path.join(location, 'image.json'), 'w') as f:
            json.dump(output, f, indent=2)

    def get_unique_keys(self, key_name):
        """
        Generate a unique list of experiment_ids from image_list
        :return: list (of unique experiment_ids)
        """
        df = pd.DataFrame(self.image_list)
        unique_ids = df[key_name].unique()
        return list(unique_ids)

    def _create_unique_fixture_from_image_list(self, json_name, key_name, model_name, location):
        """
        Internal function to be used to generate unique values from the image_list for certain keys so that
        we can create foreign look up keys
        :param json_name: str name of file to save as fixture (i.e table_name.json)
        :param key_name: str name of the key to get unique values from
        :return: list of dicts in django fixture format
        """
        if not os.path.exists(location):
            os.makedirs(location)
        unique_ids = self.get_unique_keys(key_name)
        output = []
        for i, x in enumerate(unique_ids):
            output.append(
                {
                    "model": model_name,
                    "pk": i+1,
                    "fields": {key_name: x}
                }
            )
        with open(os.path.join(location, json_name), 'w') as f:
            json.dump(output, f, indent=2)

    def create_experiment_fixture(self, location):
        """
        Creates a fixture for the repository.experiment model (i.e. experiment.json)
        :return:
        """
        self._create_unique_fixture_from_image_list(json_name='experiment.json',
                                                    key_name='experiment_id',
                                                    model_name='analytics.experiment',
                                                    location=location)

    def create_probe_fixture(self, location):
        df = pd.DataFrame(self.probe_list)
        df_sub = df[['probe_id', 'probe_name']]
        df_sub = df_sub.drop_duplicates()
        mylist = list(df_sub.T.to_dict().values())
        output = []
        for i, x in enumerate(mylist):
            output.append(
                {
                    "model": 'analytics.probe',
                    "pk": i+1,
                    "fields": x
                }
            )
        with open(os.path.join(location, 'probe.json'), 'w') as f:
            json.dump(output, f, indent=2)

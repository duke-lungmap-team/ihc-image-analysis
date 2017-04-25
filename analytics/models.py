from django.db import models
from PIL import Image
from io import BytesIO
import hashlib
import cv2
from django.core.files.uploadedfile import SimpleUploadedFile
from lungmap_sparql_client.lungmap_sparql_utils import *
import os
from tqdm import tqdm
import boto3
import tempfile
from analytics.models_choices import *

s3 = boto3.resource('s3')
bucket = s3.Bucket('lungmap-breath-data')


def get_image_from_s3(s3key):
    """
    Takes an s3key and then downloads the image, calculates a sha1, creates a SimpleUploadedFile, converts to jpeg
    and then creates another SimpleUploadedFile for the jpeg, returns 3 objects
    :param s3key: 
    :return: SimpleUploadedFile (orig), SHA1 Hash (orig), SimpleUploadedFile (jpeg converted)
    """
    try:
        s3key_jpg, ext = os.path.splitext(s3key)
        temp = tempfile.NamedTemporaryFile(suffix=ext)
        bucket.download_file(s3key, temp.name)
        cv_img = cv2.imread(temp.name)
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
        suf = SimpleUploadedFile(os.path.basename(s3key), temp_handle.read(), content_type='image/tif')
        suf_jpg = SimpleUploadedFile(
            os.path.basename(s3key_jpg) + '.jpg',
            temp_handle_jpeg.read(),
            content_type='image/jpeg'
        )
        # instance.image_orig.save(instance.s3key, suf, save=False)
        temp_handle.seek(0)
        image_orig_sha1 = hashlib.sha1(temp_handle.read()).hexdigest()
        return suf, image_orig_sha1, suf_jpg
    except ValueError as e:
        raise e


class Experiment(models.Model):
    experiment_id = models.CharField(max_length=25, primary_key=True)
    release_date = models.DateField()
    platform = models.CharField(max_length=35, blank=True, null=True)
    experiment_type = models.CharField(max_length=35, blank=True, null=True)
    # researcher = models.CharField(max_length=50, blank=True, null=True)
    # site = models.CharField(max_length=100, blank=True, null=True)
    organism = models.CharField(max_length=25)
    sex = models.CharField(max_length=20, null=True, blank=True)
    age = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s' % self.experiment_id

    def save(self, *args, **kwargs):
        try:
            metadata = get_experiment_model_data(self.experiment_id)
            self.release_date = metadata['release_date']
            self.platform = metadata['platform']
            self.experiment_type = metadata['experiment_type_label']
            # self.researcher = metadata['researcher_label']
            # self.site = metadata['site_label']
            self.organism = metadata['organism_label']
            self.sex = metadata['sex']
            self.age = metadata['age_label']
            self.validate_unique()
            super(Experiment, self).save(*args, **kwargs)
            images = get_images_by_experiment(self.experiment_id)
            expmnt = Experiment.objects.only('experiment_id').get(experiment_id=self.experiment_id)
            probes = get_probes_by_experiment(self.experiment_id)
            for probe in tqdm(probes):
                ProbeExperiments(probe_label=probe['probe_label'],
                                 color=probe['color'],
                                 experiment_id=expmnt).save()
            for image in tqdm(images):
                suf, sha1, suf_jpeg = get_image_from_s3(image['s3key'])
                LungmapImage(
                    s3key=image['s3key'],
                    magnification=image['magnification'],
                    image_name=image['image_name'],
                    experiment=expmnt,
                    image_id=image['image_id'],
                    x_scaling=image['x_scaling'],
                    y_scaling=image['y_scaling'],
                    image_orig=suf,
                    image_orig_sha1=sha1,
                    image_jpeg=suf_jpeg
                ).save()
        except ValueError as e:
            raise e


class LungmapImage(models.Model):
    s3key = models.CharField(max_length=200, unique=True)
    magnification = models.CharField(max_length=20, null=False, blank=False)
    image_name = models.CharField(max_length=80)
    experiment = models.ForeignKey(Experiment, db_column='experiment_id')
    image_id = models.CharField(max_length=40)
    x_scaling = models.CharField(max_length=65, null=True, blank=True)
    y_scaling = models.CharField(max_length=65, null=True, blank=True)
    image_orig = models.FileField(upload_to='images', blank=False, null=False)
    image_orig_sha1 = models.CharField(max_length=40, blank=False, null=False)
    image_jpeg = models.FileField(upload_to='images_jpeg', blank=False, null=False)

    def __str__(self):
        return '%s, %s' % (self.image_id, self.image_name)


class ProbeExperiments(models.Model):
    probe_label = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    experiment = models.ForeignKey(Experiment, db_column='experiment_id')

    def __str__(self):
        return '%s, %s' % (self.id, self.probe_label)

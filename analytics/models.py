from django.db import models
from PIL import Image
from io import BytesIO
import hashlib
from django.core.files.uploadedfile import SimpleUploadedFile
from lungmap_sparql_client.lungmap_sparql_utils import *
import os
import boto3
import tempfile
from analytics.models_choices import *

s3 = boto3.resource('s3')
bucket = s3.Bucket('lungmap-breath-data')


def get_from_images_from_s3(s3objkey):
    
    # metadata = get_images_by_experiment(self.experiment_id)
    temp = tempfile.NamedTemporaryFile()
    bucket.download_file(self.s3objkey, temp.name)
    img = Image.open(temp)
    img_jpeg = img.copy()
    try:
        print('inside try')
        # original image
        temp_handle = BytesIO()
        img.save(temp_handle, 'TIFF')
        temp_handle.seek(0)
        # jpeg image
        temp_handle_jpeg = BytesIO()
        img_jpeg.save(temp_handle_jpeg, 'JPEG')
        temp_handle_jpeg.seek(0)
        # filename
        filename, ext = os.path.splitext(instance.image_name)
        s3key_jpg, ext = os.path.splitext(instance.s3key)
        suf = SimpleUploadedFile(instance.image_name, temp_handle.read(), content_type='image/tif')
        suf_jpg = SimpleUploadedFile(filename + '.jpg', temp_handle_jpeg.read(), content_type='image/jpeg')
        # instance.image_orig.save(instance.s3key, suf, save=False)
        temp_handle.seek(0)
        instance.image_orig_sha1 = hashlib.sha1(temp_handle.read()).hexdigest()
        instance.image_jpeg.save(s3key_jpg + '.jpg', suf_jpg, save=False)
    except ValueError:
        print("Something went wrong with LungmapImage column image_orig upload_to function save_image.")
    upload_dir = os.path.join('image', instance.s3key, instance.image_name)
    return upload_dir


class Experiment(models.Model):
    experiment_id = models.CharField(max_length=25, primary_key=True)
    release_date = models.DateField()
    platform = models.CharField(max_length=35, blank=True, null=True)
    experiment_type = models.CharField(max_length=35, blank=True, null=True)
    # researcher = models.CharField(max_length=50, blank=True, null=True)
    # site = models.CharField(max_length=100, blank=True, null=True)
    organism = models.CharField(max_length=25)
    sex = models.CharField(max_length=20, null=True, blank=True)
    age = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.id, self.experiment_id)

    def get_metadata(self):
        return get_experiment_model_data(self.experiment_id)

    def save(self, *args, **kwargs):
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
        print(images)




class LungmapImage(models.Model):
    s3key = models.CharField(max_length=200, unique=True)
    magnification = models.CharField(max_length=20, null=False, blank=False)
    image_name = models.CharField(max_length=80)
    experiment = models.ForeignKey(Experiment, db_column='experiment_id')
    image_id = models.CharField(max_length=40)
    x_scaling = models.CharField(max_length=65, null=True, blank=True)
    y_scaling = models.CharField(max_length=65, null=True, blank=True)
    image_orig = models.FileField(upload_to='images', blank=False, null=False)
    image_orig_sha1 = models.CharField(max_length=40,blank=False, null=False)
    image_jpeg = models.FileField(upload_to='images_jpeg', blank=False, null=False)

    def __str__(self):
        return '%s, %s' % (self.image_id, self.image_name)

class ProbeExperiments(models.Model):
    probe_label = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    experiment = models.ForeignKey(Experiment, db_column='experiment_id')

    def __str__(self):
        return '%s, %s' % (self.id, self.probe_label)
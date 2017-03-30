from django.db import models
from PIL import Image
from io import BytesIO
import hashlib
from django.core.files.uploadedfile import SimpleUploadedFile
from lungmap_sparql_client.lungmap_sparql_utils import get_experiment_sample_details_first_parsed
import os
from analytics.models_choices import *


class Experiment(models.Model):
    experiment_id = models.CharField(max_length=25, unique=True)
    gender = models.CharField(max_length=20,
                              choices=GENDER_CHOICES,
                              null=False,
                              blank=False)
    age = models.CharField(max_length=10,
                           choices=AGE_CHOICES,
                           null=False,
                           blank=False)
    strain = models.CharField(max_length=20)
    genotype = models.CharField(max_length=20)
    organism = models.CharField(max_length=40,
                                choices=ORGANISM_CHOICES,
                                null=False,
                                blank=False)
    crown_rump_length = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)

    def __str__(self):
        return '%s, %s' % (self.id, self.experiment_id)

    def get_metadata(self):
        return get_experiment_sample_details_first_parsed(self.experiment_id)

    def save(self, *args, **kwargs):
        metadata = get_experiment_sample_details_first_parsed(self.experiment_id)
        self.age = metadata['age']
        self.gender = metadata['gender']
        self.strain = metadata['strain']
        self.genotype = metadata['genotype']
        self.organism = metadata['organism']
        self.crown_rump_length = metadata['crown_rump_length']
        self.weight = metadata['weight']
        self.validate_unique()
        super(Experiment, self).save(*args, **kwargs)


def save_image(instance, filename):

    img = Image.open(instance.image_orig)
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


class LungmapImage(models.Model):
    s3key = models.CharField(max_length=200, unique=True)
    magnification = models.CharField(max_length=20,
                                     choices=MAGNIFICATION_CHOICES,
                                     null=False,
                                     blank=False)
    image_name = models.CharField(max_length=80)
    experiment = models.ForeignKey(Experiment)
    image_id = models.CharField(max_length=40)
    date = models.DateField()
    image_orig = models.FileField(upload_to=save_image,
                                  blank=False,
                                  null=False)
    image_orig_sha1 = models.CharField(max_length=40,
                                       blank=False,
                                       null=False)
    image_jpeg = models.FileField(upload_to='images_jpeg',
                                  blank=False,
                                  null=False)

    def __str__(self):
        return '%s, %s' % (self.image_id, self.image_name)

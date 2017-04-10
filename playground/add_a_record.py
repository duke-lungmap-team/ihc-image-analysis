import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "lap.settings")
import django
django.setup()

from analytics.models import LungmapImage, Experiment
from analytics.serializers import LungmapImageSerializer, ExperimentSerializer
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('lungmap-breath-data')

serializer = LungmapImageSerializer()

exp_ser = ExperimentSerializer()

img = Image.open('/Users/nn31/Documents/ihc-image-analysis/media/images/LMEX0000000688/fibronectin_p21_x40/fibronectin_p21_x40.tif')
temp_handle = BytesIO()
img.save(temp_handle, 'TIFF')
temp_handle.seek(0)
suf = SimpleUploadedFile('laminin_p28_x40.tif', temp_handle.read(), content_type='image/tif')

entry = Experiment.objects.get(pk=1)

snippet = LungmapImage(s3key='LMEX0000000695/laminin_p28_x40/laminin_p28_x40.tif',
                       strain='C57BL6',
                       organism='mus musculus',
                       magnification='20X',
                       image_name='laminin_p28_x40.tif',
                       gender='male',
                       age='E18.5',
                       experiment=entry,
                       image_id='LMEX0000000695_IMG_1',
                       date='2016-03-17',
                       image_orig = suf)
snippet.save()


####

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "lap.settings")
import django
django.setup()
from analytics.models import Experiment

test = Experiment(experiment_id='LMEX0000000004')

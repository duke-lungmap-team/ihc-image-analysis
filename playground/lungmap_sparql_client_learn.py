from lungmap_sparql_client.lungmap_sparql_utils import *

#get all experiments
experiments = list_all_lungmap_experiments()

#get images from an experiment
images = get_images_by_experiment('LMEX0000000024')
probes = get_probes_by_experiment('LMEX0000000679')

types = get_experiment_type_by_experiment('LMEX0000000274')
a = get_experiment_model_data('LMEX0000000274')

researcher = get_researcher_by_experiment('LMEX0000000679')
sample = get_sample_by_experiment('LMEX0000000679')

experiment_data = get_experiment_model_data('LMEX0000000679')

import boto3
from PIL import Image
import cv2
import os
import tempfile
from io import BytesIO
import hashlib
from django.core.files.uploadedfile import SimpleUploadedFile

s3 = boto3.resource('s3')
bucket = s3.Bucket('lungmap-breath-data')
s3key = 'LMEX0000000024/2015-003-026_20X_C57Bl6_E16.5_LMM.14.24.4.41_CSPG4_NKX2.1_ACTA2_001/2015-003-026_20X_C57Bl6_E16.5_LMM.14.24.4.41_CSPG4_NKX2.1_ACTA2_001.tif'
s3key_jpg, ext = os.path.splitext(s3key)
orig_img = tempfile.NamedTemporaryFile(suffix=ext)
bucket.download_file(s3key, orig_img.name)

#what do we want to do here - i think defaults to 1 which converts to 8bit
    # CV_LOAD_IMAGE_UNCHANGED  =-1,
    # CV_LOAD_IMAGE_GRAYSCALE  =0,
    # CV_LOAD_IMAGE_COLOR      =1,
    # CV_LOAD_IMAGE_ANYDEPTH   =2,
    # CV_LOAD_IMAGE_ANYCOLOR   =4

img = cv2.imread(orig_img.name)
orig_img.close()
f = BytesIO(img.tobytes())
f.seek(0)
suf = SimpleUploadedFile('test3.tif', f.read(), content_type='image/tif')
f.seek(0)
image_orig_sha1 = hashlib.sha1(f.read()).hexdigest()
jpeg_img = tempfile.NamedTemporaryFile(suffix='.jpg')
cv2.imwrite(jpeg_img.name,img)



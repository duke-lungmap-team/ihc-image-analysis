import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "lap.settings")
import django
django.setup()
from analytics.models import Experiment, LungmapImage, get_image_from_s3, ProbeExperiments
from analytics.serializers import ExperimentSerializer, LungmapImageSerializer
from lungmap_sparql_client.lungmap_sparql_utils import *
#what experiments does lungmap have?
lm_experiments = list_all_lungmap_experiments()

a = Experiment(experiment_id='LMEX0000000062')
print(ExperimentSerializer(a).data)
a.save()

# expmnt = Experiment.objects.only('experiment_id').get(experiment_id='LMEX0000000062')
#
# probes = get_probes_by_experiment('LMEX0000000062')
# probe = probes[0]
#
# a = ProbeExperiments(probe_label=probe['probe_label'],
#                 color = probe['color'],
#                 experiment_id = expmnt).save()

# images = get_images_by_experiment('LMEX0000000062')
# image = images[0]
# suf, sha1, suf_jpeg = get_image_from_s3(image['s3key'])
# expmnt = Experiment.objects.only('experiment_id').get(experiment_id=image['experiment_id'])
#
# a_img = LungmapImage(s3key = image['s3key'],
#     magnification = image['magnification'],
#     image_name = image['image_name'],
#     experiment = expmnt,
#     image_id = image['image_id'],
#     x_scaling = image['x_scaling'],
#     y_scaling = image['y_scaling'],
#     image_orig = suf,
#     image_orig_sha1 = sha1,
#     image_jpeg = suf_jpeg)
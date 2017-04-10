from analytics.models import Experiment, LungmapImage
from analytics.serializers import ExperimentSerializer, LungmapImageSerializer
from lungmap_sparql_client.lungmap_sparql_utils import *
#what experiments does lungmap have?
lm_experiments = list_all_lungmap_experiments()

a = Experiment(experiment_id='LMEX0000000671')
a.save()

#Image
image_a = LungmapImage(experiment_id='LMEX0000000671')
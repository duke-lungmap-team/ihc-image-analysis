from lungmap_sparql_client.lungmap_sparql_utils import *

#get all experiments
experiments = list_all_lungmap_experiments()

#get images from an experiment
images = get_images_by_experiment('LMEX0000000679')
probes = get_probes_by_experiment('LMEX0000000679')

types = get_experiment_type_by_experiment('LMEX0000000274')
a = get_experiment_model_data('LMEX0000000274')

researcher = get_researcher_by_experiment('LMEX0000000679')
sample = get_sample_by_experiment('LMEX0000000679')

experiment_data = get_experiment_model_data('LMEX0000000679')
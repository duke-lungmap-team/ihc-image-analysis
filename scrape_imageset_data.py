from lungmap_client import lungmap_sparql_queries as sparql_queries
from lungmap_client import lungmap_utils
from tqdm import tqdm
from analytics import models

output = []
exp_names_df = lungmap_utils.list_all_lungmap_experiments()
#experiment = exp_names_df[0]
for experiment in tqdm(exp_names_df):
    results = lungmap_utils._get_by_experiment(
            sparql_queries.GET_PROBE_BY_EXPERIMENT,
            experiment
    )
    probes = [(x['probe_label']['value'],x['color']['value']) for x in results]
    experiment_data = lungmap_utils.get_sample_by_experiment(experiment)
    images = lungmap_utils.get_images_by_experiment(experiment)
    magnifications = list(set(([x['magnification'] for x in images])))
    for x in magnifications:
        try:
            #TODO: probes really should be set(probes) so that order doesn't matter. However, set(probes) results in
            #more cases below, so we leave as a list for now
            document = {'probes': probes,
                        'species': experiment_data['organism_label'],
                        'age': experiment_data['age_label'],
                        'magnification': x,
                        'experiments': [experiment]}
            output.append(document)
        except:
            continue



from itertools import groupby
from operator import itemgetter

def deduplicate_our_list(grouper_vars,input_list):
    """
    returns a list deduplicated by experiment_id
    :param grouper:
    :param input_list:
    :return:
    """
    grouper = itemgetter(*grouper_vars)
    result = []
    for key, grp in groupby(sorted(input_list, key = grouper), grouper):
        temp_dict = dict(zip(grouper_vars, key))
        all_exp = []
        for item in grp:
            all_exp.extend(item['experiments'])
        temp_dict["experiments"] = all_exp
        result.append(temp_dict)
    return result

#TODO: consider adding age? We said this in the meeting, but essentially this means that every experiment cannot be
#consolidated into broader groupings.
grouper_vars = ["magnification", "probes", "species"]
result = deduplicate_our_list(grouper_vars, output)

#now time to load up the tables!
#Load
#     experiment
#     probe
#     experimentprobemap
#     imageset
#
#
# for x in result:
#     for y in x['experiments']:
#         exp_obj, exp_created = models.Experiment.objects.get_or_create(
#             experiment_id = y
#         )
#     for z in x['probes']:
#         prob_obj, prob_created = models.Probe.objects.get_or_create(
#             label = z[0].rstrip()
#         )
#
# metadata = lungmap_utils.get_experiment_model_data(y)
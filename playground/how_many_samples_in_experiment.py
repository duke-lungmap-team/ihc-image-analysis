from lungmap_sparql_client.lungmap_sparql_client import *
from lungmap_sparql_client.lungmap_sparql_utils import *
import pandas as pd

alldata_df = pd.DataFrame(LMClient.create_image_table(get_lungmap_file_list_all))
exp_names_df = alldata_df[['experiment_id']].drop_duplicates()
samples = {}
for x in list(exp_names_df['experiment_id']):
    samples[x] = get_experiment_sample_details(x)

for key, value in samples.items():
    if len(value['bindings'])>1:
        print(key + ' ' + str(len(value['bindings'])))

look = samples['LMEX0000000858']



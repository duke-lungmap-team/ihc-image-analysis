from lungmap_client import lungmap_utils
from analytics import models as mymodels

image_sets = lungmap_utils.get_image_set_candidates()

# key = 'mus musculus_P07_60X_Acetylated Tubulin__White_CCSP __Red_TTF-1__Green'
# value = image_sets[key]

for key, value in image_sets.items():
    print('loading imageset ', key)
    image_set = mymodels.ImageSet.objects.create(
        image_set_name = key,
        magnification = value['magnification'],
        species = value['species'],
        development_stage = value['development_stage']
    )
    for image in value['images']:
        experiment, experiment_create = mymodels.Experiment.objects.get_or_create(
            experiment_id = image['image_id'].split('_')[0]
        )
        imageobject = mymodels.Image.objects.create(
            s3key = image['s3key'],
            image_name = image['image_name'],
            image_id = image['image_id'],
            x_scaling = image['x_scaling'],
            y_scaling = image['y_scaling'],
            image_set = image_set,
            experiment_id = experiment
        )
    for probe in value['probes']:
        probeobject, probeobject_create = mymodels.Probe.objects.get_or_create(
            label = probe['probe_label']
        )
        imagesetprobemap = mymodels.ImageSetProbeMap.objects.create(
            color = probe['color'],
            probe_name = probeobject,
            image_set = image_set
        )
        for exp in value['experiments']:
            experimentobject = mymodels.Experiment.objects.get(
                experiment_id = exp
            )
            experimentprobemap = mymodels.ExperimentProbeMap.objects.create(
                color = probe['color'],
                experiment_id = experimentobject,
                probe_name=probeobject,
            )



#Load Experiments


#Load Probes
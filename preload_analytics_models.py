from lungmap_client import lungmap_utils
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lap.settings")
django.setup()

from analytics import models


image_sets = lungmap_utils.get_image_set_candidates()

for key, value in image_sets.items():
    print('loading image set ', key)

    image_set = models.ImageSet.objects.get_or_create(
        image_set_name=key,
        magnification=value['magnification'],
        species=value['species'],
        development_stage=value['development_stage']
    )

    for image in value['images']:
        experiment, experiment_create = models.Experiment.objects.get_or_create(
            experiment_id=image['image_id'].split('_')[0]
        )

        image_object = models.Image.objects.get_or_create(
            s3key=image['s3key'],
            image_name=image['image_name'],
            image_id=image['image_id'],
            x_scaling=image['x_scaling'],
            y_scaling=image['y_scaling'],
            image_set=image_set[0],
            experiment_id=experiment.experiment_id
        )

    for p in value['probes']:
        probe_object, probe_object_create = models.Probe.objects.get_or_create(
            label=p['probe_label']
        )

        image_set_probe_map = models.ImageSetProbeMap.objects.get_or_create(
            color=p['color'],
            probe=probe_object,
            image_set=image_set[0]
        )

        for exp in value['experiments']:
            experiment_object = models.Experiment.objects.get(
                experiment_id=exp
            )

            experiment_probe_map = models.ExperimentProbeMap.objects.create(
                color=p['color'],
                experiment_id=experiment_object,
                probe=probe_object,
            )


# need to fill in with actual data from ontology
def add_probe_anatomy(probe, class_name):
    """
    Add a probe/classification combo, this can be either cell or stucture as identified
    by the class_type
    :param probe: str: a probe name
    :param class_name: str: a classficiation name
    :return:
    """
    probe_instance = models.Probe.objects.get(label=probe)
    anatomy = models.Anatomy.objects.create(name=class_name)

    models.AnatomyProbeMap.objects.create(
        probe=probe_instance,
        anatomy=anatomy
    )

add_probe_anatomy('Sox2', 'bronchiolar_epithelial_cell')
add_probe_anatomy('TTF-1', 'epithelial_cell_of_the_lung')
add_probe_anatomy('α-Smooth Muscle Actin', 'bronchiolar-associated_smooth_muscle_cell')
add_probe_anatomy('α-Smooth Muscle Actin', 'bronchiole')
add_probe_anatomy('Sox9', 'distal_acinar_tubule')
add_probe_anatomy('α-Smooth Muscle Actin', 'proximal_acinar_tubule')
add_probe_anatomy('α-Smooth Muscle Actin', 'blood_vessel')

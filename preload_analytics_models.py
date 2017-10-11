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
            experiment_id=image['experiment_id'],
            experiment_type_id=image['experiment_type_id']
        )

        image_object = models.Image.objects.get_or_create(
            source_url=image['source_url'],
            image_name=image['image_name'],
            image_id=image['image_id'],
            x_scaling=image['x_scaling'],
            y_scaling=image['y_scaling'],
            image_set=image_set[0],
            experiment_id=experiment.experiment_id
        )

    for p in value['probes']:
        probe_object, probe_object_create = models.Probe.objects.get_or_create(
            label=p['probe_label'].strip()
        )

        image_set_probe_map = models.ImageSetProbeMap.objects.get_or_create(
            color=p['color'],
            probe=probe_object,
            image_set=image_set[0]
        )

        for exp in value['experiments']:
            experiment_object = models.Experiment.objects.get(
                experiment_id=exp['experiment_id']
            )

            experiment_probe_map = models.ExperimentProbeMap.objects.create(
                color=p['color'],
                experiment_id=experiment_object,
                probe=probe_object,
            )

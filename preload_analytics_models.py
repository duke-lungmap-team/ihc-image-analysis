from lungmap_client import lungmap_utils
import django

django.setup()

from analytics import models


image_sets = lungmap_utils.get_image_set_candidates()

for key, value in image_sets.items():
    print('loading imageset ', key)
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
        imageobject = models.Image.objects.get_or_create(
            s3key=image['s3key'],
            image_name=image['image_name'],
            image_id=image['image_id'],
            x_scaling=image['x_scaling'],
            y_scaling=image['y_scaling'],
            image_set=image_set[0],
            experiment_id=experiment.experiment_id
        )

    for probe in value['probes']:
        probeobject, probeobject_create = models.Probe.objects.get_or_create(
            label=probe['probe_label']
        )
        imagesetprobemap = models.ImageSetProbeMap.objects.get_or_create(
            color=probe['color'],
            probe=probeobject,
            image_set=image_set[0]
        )

        for exp in value['experiments']:
            experimentobject = models.Experiment.objects.get(
                experiment_id=exp
            )
            experimentprobemap = models.ExperimentProbeMap.objects.create(
                color=probe['color'],
                experiment_id=experimentobject,
                probe=probeobject,
            )

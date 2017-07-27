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

#need to fill in with actual data from ontology
def add_probe_classification(probe, class_name, class_type):
    """
    Add a probe/classification combo, this can be either cell or stucture as identified
    by the class_type
    :param probe: str: a probe name
    :param class_name: str: a classficiation name
    :param class_type: str: either 'cell' or 'structure'
    :return:
    """
    probe_instance = models.Probe.objects.get(label=probe)
    if class_type == 'structure':
        structure = models.Structure.objects.create(structure_name=class_name)
        ps_mapping = models.StructureProbeMap.objects.create(
            probe = probe_instance,
            structure = structure
        )
    elif class_type == 'cell':
        cell = models.Cell.objects.create(cell_name=class_name)
        pc_mapping = models.CellProbeMap.objects.create(
            probe = probe_instance,
            cell = cell
        )

add_probe_classification('Sox2', 'bronchiolar_epithelial_cell', 'cell')
add_probe_classification('TTF-1', 'epithelial_cell_of_the_lung', 'cell')
add_probe_classification('α-Smooth Muscle Actin', 'bronchiolar-associated_smooth_muscle_cell', 'cell')
add_probe_classification('α-Smooth Muscle Actin', 'bronchiole', 'structure')
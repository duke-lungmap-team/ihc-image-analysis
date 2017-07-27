from django.db import models
from lungmap_client import lungmap_utils as sparql_utils


class Experiment(models.Model):
    experiment_id = models.CharField(
        max_length=25,
        primary_key=True
    )
    platform = models.CharField(
        max_length=35,
        blank=True,
        null=True
    )
    experiment_type = models.CharField(
        max_length=35,
        blank=True,
        null=True
    )
    sex = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s' % self.experiment_id

    def save(self, *args, **kwargs):
        try:
            metadata = sparql_utils.get_experiment_model_data(self.experiment_id)
            self.platform = metadata['platform']
            self.experiment_type = metadata['experiment_type_label']
            self.sex = metadata['sex']

            super(Experiment, self).save(*args, **kwargs)
        except ValueError as e:
            raise e


class ImageSet(models.Model):
    image_set_name = models.CharField(
        unique=True,
        max_length=200,
        null=False,
        blank=False
    )
    magnification = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    species = models.CharField(
        max_length=25
    )
    development_stage = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )


class Probe(models.Model):
    label = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True
    )

    def __str__(self):
        return '%s: %s' % (self.id, self.label)


class ImageSetProbeMap(models.Model):
    image_set = models.ForeignKey(ImageSet)
    probe = models.ForeignKey(Probe)
    color = models.CharField(
        max_length=30
    )


class Image(models.Model):
    s3key = models.CharField(
        max_length=200
    )
    image_name = models.CharField(max_length=200)
    image_set = models.ForeignKey(ImageSet)
    experiment = models.ForeignKey(Experiment)
    image_id = models.CharField(max_length=40)
    x_scaling = models.CharField(
        max_length=65,
        null=True,
        blank=True
    )
    y_scaling = models.CharField(
        max_length=65,
        null=True,
        blank=True
    )
    image_orig = models.FileField(
        upload_to='images',
        blank=True,
        null=True
    )
    image_orig_sha1 = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    image_jpeg = models.FileField(
        upload_to='images_jpeg',
        blank=True,
        null=True
    )

    def __str__(self):
        return '%s, %s' % (self.image_id, self.image_name)


class ExperimentProbeMap(models.Model):
    probe = models.ForeignKey(Probe)
    color = models.CharField(max_length=30)
    experiment = models.ForeignKey(Experiment)

    def __str__(self):
        return '%s, %s (%s)' % (self.experiment_id, self.probe.label, self.color)


class Subregion(models.Model):
    image = models.ForeignKey(Image)

    def __str__(self):
        return '%s, %s' % (
            self.id,
            self.image.image_name,
        )


class Points(models.Model):
    subregion = models.ForeignKey(Subregion)
    x = models.IntegerField()
    y = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return '%s %s #%s: [%s, %s]' % (self.id, self.subregion_id, self.order, self.x, self.y)


class Cell(models.Model):
    cell_name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return '%s: %s' % (self.id, self.cell_name)


class CellProbeMap(models.Model):
    probe = models.ForeignKey(Probe)
    cell = models.ForeignKey(Cell)

    def __str__(self):
        return '%s: <Probe: %s>, <Cell: %s>' % (self.id,
                                                self.probe.label,
                                                self.cell.cell_name)


class Structure(models.Model):
    structure_name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return '%s: %s' % (self.id, self.structure_name)


class StructureProbeMap(models.Model):
    structure = models.ForeignKey(Structure)
    probe = models.ForeignKey(Probe)

    def __str__(self):
        return '%s: <Probe: %s>, <Structure: %s>' % (self.id,
                                                     self.probe.label,
                                                     self.structure.structure_name)

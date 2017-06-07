from django.db import models
from lungmap_client import lungmap_utils as sparql_utils


class Experiment(models.Model):
    experiment_id = models.CharField(
        max_length=25,
        primary_key=True
    )
    release_date = models.DateField()
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
    organism = models.CharField(max_length=25)
    sex = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    age = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s' % self.experiment_id

    def save(self, *args, **kwargs):
        try:
            metadata = sparql_utils.get_experiment_model_data(self.experiment_id)
            self.release_date = metadata['release_date']
            self.platform = metadata['platform']
            self.experiment_type = metadata['experiment_type_label']
            self.organism = metadata['organism_label']
            self.sex = metadata['sex']
            self.age = metadata['age_label']

            super(Experiment, self).save(*args, **kwargs)
        except ValueError as e:
            raise e


class Probe(models.Model):
    label = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True
    )

    def __str__(self):
        return '%s: %s' % (self.id, self.label)


class Image(models.Model):
    s3key = models.CharField(
        max_length=200,
        unique=True
    )
    magnification = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    image_name = models.CharField(max_length=80)
    experiment = models.ForeignKey(
        Experiment,
        db_column='experiment_id'
    )
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
        blank=False,
        null=False
    )
    image_orig_sha1 = models.CharField(
        max_length=40,
        blank=False,
        null=False
    )
    image_jpeg = models.FileField(
        upload_to='images_jpeg',
        blank=False,
        null=False
    )

    def __str__(self):
        return '%s, %s' % (self.image_id, self.image_name)


class ExperimentProbeMap(models.Model):
    probe = models.ForeignKey(Probe)
    color = models.CharField(max_length=30)
    experiment = models.ForeignKey(
        Experiment,
        db_column='experiment_id'
    )

    def __str__(self):
        return '%s, %s (%s)' % (self.experiment_id, self.probe.label, self.color)


class Classification(models.Model):
    classification_name = models.CharField(
        max_length=100
    )
    def __str__(self):
        return '%s: %s' % (self.id, self.classification_name)


class Subregion(models.Model):
    classification = models.ForeignKey(
        Classification,
        related_name='subregion',
        db_column='classification_id'
    )
    image = models.ForeignKey(
        Image,
        db_column='image_id'
    )

    def __str__(self):
        return '%s, %s, %s' % (self.id, self.image_id.image_name, self.classification_id.classification_name)


class Points(models.Model):
    subregion = models.ForeignKey(
        Subregion,
        related_name='points',
        db_column='subregion_id'
    )
    x = models.IntegerField()
    y = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return '%s %s #%s: [%s, %s]' % (self.id, self.subregion_id, self.order, self.x, self.y)

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Experiment(models.Model):
    experiment_id = models.CharField(
        max_length=25,
        primary_key=True
    )
    experiment_type_id = models.CharField(
        max_length=35,
        blank=False,
        null=False
    )
    species = models.CharField(
        max_length=25
    )

    def __str__(self):
        return '%s' % self.experiment_id


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

    def __str__(self):
        return '%s' % self.id

    def get_subregion_count(self):
        return Subregion.objects.filter(image__image_set=self).count()

    def get_images_with_subregion_count(self):
        return Image.objects.annotate(subregion_count=models.Count('subregion')).filter(
            image_set=self,
            subregion_count__gt=0
        ).count()

    def get_images_with_subregion_count_by_anatomy_name(self):
        return Subregion.objects.filter(image__image_set=self)\
            .values('anatomy__name') \
            .annotate(total=models.Count('anatomy__name')) \
            .order_by('anatomy__name')


class Probe(models.Model):
    label = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    species = models.CharField(
        max_length=25
    )

    class Meta:
        unique_together = (('label', 'species'),)

    def __str__(self):
        return '%s: %s' % (self.id, self.label)


class ImageSetProbeMap(models.Model):
    image_set = models.ForeignKey(ImageSet)
    probe = models.ForeignKey(Probe)
    color = models.CharField(
        max_length=30
    )


class Image(models.Model):
    source_url = models.CharField(
        max_length=400
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


class OntoEntityType(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        unique=True
    )


class OntoEntity(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        unique=True
    )
    type = models.ForeignKey(OntoEntityType)

    def __str__(self):
        return '%s (%s)' % (self.name, self.type.name)


class OntoEntityMap(models.Model):
    entity = models.ForeignKey(OntoEntity)
    has_part = models.ForeignKey(OntoEntity, related_name='has_part')

    class Meta:
        unique_together = (('entity', 'has_part'),)


class ProbeOntoProteinMap(models.Model):
    probe = models.ForeignKey(Probe)
    protein = models.ForeignKey(OntoEntity)

    class Meta:
        unique_together = (('probe', 'protein'),)


class Anatomy(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class AnatomyProbeMap(models.Model):
    probe = models.ForeignKey(Probe)
    anatomy = models.ForeignKey(Anatomy)

    class Meta:
        unique_together = (('probe', 'anatomy'),)

    def __str__(self):
        return '%s: <Probe: %s>, <Anatomy: %s>' % (self.id,
                                                   self.probe.label,
                                                   self.anatomy.name)


# temporary new Subregion model
class SubregionNew(models.Model):
    image = models.ForeignKey(Image)
    entity = models.ForeignKey(OntoEntity)
    user = models.ForeignKey(
        User,
        null=False,
        blank=False
    )

    def __str__(self):
        return '%s, %s' % (
            self.id,
            self.image.image_name,
        )


class Subregion(models.Model):
    image = models.ForeignKey(Image)
    anatomy = models.ForeignKey(Anatomy)
    user = models.ForeignKey(
        User,
        null=False,
        blank=False
    )

    def __str__(self):
        return '%s, %s' % (
            self.id,
            self.image.image_name,
        )


class Points(models.Model):
    subregion = models.ForeignKey(
        Subregion,
        related_name='points',
        on_delete=models.CASCADE
    )
    x = models.IntegerField()
    y = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return '%s %s #%s: [%s, %s]' % (self.id, self.subregion_id, self.order, self.x, self.y)


class TrainedModel(models.Model):
    imageset = models.OneToOneField(ImageSet)
    model_object = models.FileField(
        upload_to='trained_models',
        blank=True,
        null=True
    )

    def __str__(self):
        return '<TrainedModel %s: %s' % (self.id, self.imageset_id)

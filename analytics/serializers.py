from rest_framework import serializers
from analytics import models
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class ImageSerializer(serializers.ModelSerializer):
    image_jpeg = serializers.HyperlinkedIdentityField('image-jpeg', read_only=True)

    class Meta:
        model = models.Image
        fields = "__all__"


class TrainedModelSerializer(serializers.ModelSerializer):
    trained_model_id = serializers.CharField(source='id')

    class Meta:
        model = models.TrainedModel
        fields = ["trained_model_id"]


class TrainedModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TrainedModel
        fields = ['imageset']


class ImageSetProbeMapSerializer(serializers.ModelSerializer):
    probe_label = serializers.CharField(source='probe.label')

    class Meta:
        model = models.ImageSetProbeMap
        fields = ['color', 'probe', 'probe_label']


class ImageSetSerializer(serializers.ModelSerializer):
    model = TrainedModelSerializer(source='trainedmodel')
    probes = ImageSetProbeMapSerializer(source='imagesetprobemap_set', many=True)
    images = ImageSerializer(source='image_set', many=True)

    class Meta:
        model = models.ImageSet
        fields = ('id', 'image_set_name', 'magnification', 'species',
                  'development_stage', 'probes', 'images', 'model')


class ExperimentSerializer(serializers.ModelSerializer):
    experiment_id = serializers.CharField(max_length=14, required=True)
    platform = serializers.CharField(read_only=True)
    experiment_type = serializers.CharField(read_only=True)
    sex = serializers.CharField(read_only=True)

    class Meta:
        model = models.Experiment
        fields = "__all__"


class ProbeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Probe
        fields = "__all__"


class ExperimentProbeSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='probe.label')

    class Meta:
        model = models.ExperimentProbeMap
        fields = "__all__"


class PointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Points
        fields = ('x', 'y', 'order')


class SubregionSerializer(serializers.ModelSerializer):
    points = PointsSerializer(many=True)

    class Meta:
        model = models.Subregion
        fields = ["image", "anatomy", "points"]

    def create(self, validated_data):
        subregion = models.Subregion.objects.create(**validated_data)
        return subregion


class ClassifyPointsSerializer(serializers.ModelSerializer):
    points = PointsSerializer(source='subregion_set__points_set', many=True)
    image_id = serializers.CharField(source='id')

    class Meta:
        model = models.Image
        fields = ['points', 'image_id']


class AnatomyProbeMapSerializer(serializers.ModelSerializer):
    anatomy_name = serializers.CharField(source='anatomy.name')
    anatomy_id = serializers.CharField(source='anatomy.id')
    probe_id = serializers.CharField(source='probe.id')

    class Meta:
        model = models.AnatomyProbeMap
        fields = ['anatomy_name', 'anatomy_id', 'probe_id']


class AnatomySerializer(serializers.ModelSerializer):
    anatomies = AnatomyProbeMapSerializer(source='anatomyprobemap_set', many=True)

    class Meta:
        model = models.Probe
        fields = ['anatomies']


class AnatomyModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Anatomy
        fields = "__all__"


class SubregionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subregion
        fields = "__all__"


class ImageSubregionSerializers(serializers.ModelSerializer):
    image_id = serializers.CharField(source='id')
    subregion_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = ['image_id', 'subregion_count']

    # noinspection PyMethodMayBeStatic
    def get_subregion_count(self, obj):
        return obj.subregion_set.count()


# noinspection PyAbstractClass
class SubregionAnatomyAggregationSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    anatomy_id = serializers.IntegerField()
    anatomy__name = serializers.CharField()

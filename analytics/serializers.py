from rest_framework import serializers
from analytics import models
from django.contrib.auth.models import User
import pprint


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class ImageSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ImageSet
        fields = "__all__"


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


class LungmapImageSerializer(serializers.ModelSerializer):
    image_jpeg = serializers.HyperlinkedIdentityField('image-jpeg', read_only=True)

    class Meta:
        model = models.Image
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
        points_data = validated_data.pop('points')
        subregion = models.Subregion.objects.create(**validated_data)
        for point_data in points_data:
            point = models.Points.objects.create(subregion=subregion,
                                                 **point_data)
        return subregion


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = "__all__"


class ProbeNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Probe
        fields = ['label']


class ImageSetProbeMapSerializer(serializers.ModelSerializer):
    probe_label = serializers.CharField(source='probe.label')

    class Meta:
        model = models.ImageSetProbeMap
        fields = ['color', 'probe', 'probe_label']


class ImageSetDetailSerializer(serializers.ModelSerializer):
    probes = ImageSetProbeMapSerializer(source='imagesetprobemap_set', many=True)
    images = LungmapImageSerializer(source='image_set', many=True)

    class Meta:
        model = models.ImageSet
        fields = ('image_set_name', 'magnification', 'species',
                  'development_stage', 'probes', 'images')


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
        model=models.Image
        fields = ['image_id', 'subregion_count']

    def get_subregion_count(self, obj):
        return obj.subregion_set.count()


class CountImages(serializers.ModelSerializer):
    imageset_name = serializers.CharField(source='image_set_name')
    imageset_id = serializers.CharField(source='id')
    images = ImageSubregionSerializers(source='image_set', many=True)

    class Meta:
        model = models.ImageSet
        fields = ['imageset_name', 'imageset_id', 'images']


class SubregionAnatomyAggregationSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    anatomy_id = serializers.IntegerField()
    anatomy__name = serializers.CharField()








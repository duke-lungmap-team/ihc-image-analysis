from rest_framework import serializers
from analytics import models
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class ExperimentSerializer(serializers.ModelSerializer):
    experiment_id = serializers.CharField(max_length=14, required=True)
    release_date = serializers.DateField(read_only=True)
    platform = serializers.CharField(read_only=True)
    experiment_type = serializers.CharField(read_only=True)
    organism = serializers.CharField(read_only=True)
    sex = serializers.CharField(read_only=True)
    age = serializers.CharField(read_only=True)

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
    id = serializers.CharField(read_only=True)
    points = PointsSerializer(many=True)

    class Meta:
        model = models.Subregion
        fields = ('id', 'classification', 'image', 'points')

    def to_representation(self, instance):
        data = super(SubregionSerializer, self).to_representation(instance)
        data['image'] = instance.image.image_name
        data['classification'] = instance.classification.classification_name
        return data

    def create(self, validated_data):
        points_data = validated_data.pop('points')
        subregion = models.Subregion.objects.create(**validated_data)
        for point_data in points_data:
            models.Points.objects.create(subregion=subregion, **point_data)
        return subregion


class ClassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Classification
        fields = "__all__"
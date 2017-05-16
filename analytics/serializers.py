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

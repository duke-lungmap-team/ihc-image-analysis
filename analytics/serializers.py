from rest_framework import serializers
from analytics.models import Experiment, LungmapImage, ProbeExperiments
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class ExperimentSerializer(serializers.ModelSerializer):
    experiment_id = serializers.CharField(required=True)
    release_date = serializers.DateField(read_only=True)
    platform = serializers.CharField(read_only=True)
    experiment_type = serializers.CharField(read_only=True)
    organism = serializers.CharField(read_only=True)
    sex = serializers.CharField(read_only=True)
    age = serializers.CharField(read_only=True)

    class Meta:
        model = Experiment
        fields = "__all__"

# class ExperimentIdSerializer(serializers.ModelSerializer):
#
#     experiment_id = serializers.CharField(required=True)
#
#     class Meta:
#         model = Experiment
#         fields = ("experiment_id",)

class ProbeExperimentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProbeExperiments
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = LungmapImage
        fields = "__all__"


class LungmapImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = LungmapImage
        fields = "__all__"

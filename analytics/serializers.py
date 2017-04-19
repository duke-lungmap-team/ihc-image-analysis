from rest_framework import serializers
from analytics.models import Experiment, LungmapImage, ProbeExperiments
from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Experiment.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'snippets')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')

class ExperimentSerializer(serializers.ModelSerializer):

    experiment_id = serializers.CharField(required=True)

    class Meta:
        model = Experiment
        fields = "__all__"

class ExperimentIdSerializer(serializers.ModelSerializer):

    experiment_id = serializers.CharField(required=True)

    class Meta:
        model = Experiment
        fields = ("experiment_id",)

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

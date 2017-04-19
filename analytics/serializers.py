from rest_framework import serializers
from analytics.models import Experiment, LungmapImage, ProbeExperiments


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


class LungmapImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = LungmapImage
        fields = "__all__"

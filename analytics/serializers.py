from rest_framework import serializers
from analytics.models import Experiment, Probe, LungmapImage


class ExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experiment
        fields = ('id', 'experiment_id')


class ProbeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Probe
        fields = ('id', 'probe_name', 'probe_id')


class LungmapImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = LungmapImage
        fields = (
            'id',
            's3key',
            'strain',
            'organism',
            'magnification',
            'image_name',
            'gender',
            'age',
            'experiment',
            'image_id',
            'date',
            'image_orig'
        )

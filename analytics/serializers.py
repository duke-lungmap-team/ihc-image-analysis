from rest_framework import serializers
from analytics.models import Experiment, LungmapImage


class ExperimentSerializer(serializers.ModelSerializer):

    experiment_id = serializers.CharField(required=True)
    gender = serializers.CharField(read_only=True)
    age = serializers.CharField(read_only=True)
    strain = serializers.CharField(read_only=True)
    genotype = serializers.CharField(read_only=True)
    organism = serializers.CharField(read_only=True)
    crown_rump_length = serializers.CharField(read_only=True)
    weight = serializers.CharField(read_only=True)

    class Meta:
        model = Experiment
        fields = (
            'id',
            'experiment_id',
            'gender',
            'age',
            'strain',
            'genotype',
            'organism',
            'crown_rump_length',
            'weight'
        )


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

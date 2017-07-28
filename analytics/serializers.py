from rest_framework import serializers
from analytics import models
from django.contrib.auth.models import User


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
    class Meta:
        model = models.Subregion
        fields = "__all__"

# class SubregionSerializer(serializers.ModelSerializer):
#
#     points = PointsSerializer(many=True)
#
#     class Meta:
#         model = models.Subregion
#         fields = ('id', 'image', 'points')
#
#     def to_representation(self, instance):
#         data = super(SubregionSerializer, self).to_representation(instance)
#         data['image'] = instance.image.image_name
#         return data
#
#     def create(self, validated_data):
#         points_data = validated_data.pop('points')
#         subregion = models.Subregion.objects.create(**validated_data)
#         for point_data in points_data:
#             models.Points.objects.create(subregion=subregion, **point_data)
#         return subregion


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


class CellSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cell
        fields = ['cell_name']


class StructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Structure
        fields = ['structure_name']


class ImagesetLabelSerializer(serializers.ModelSerializer):
    cells = serializers.SerializerMethodField()
    structures = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.cellinstances, self.structureinstances = self.get_rel(args[0])
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.ImageSet
        fields = ['cells', 'structures']

    def get_rel(self, obj):
        im_probe_query_set = models.ImageSetProbeMap.objects.filter(image_set_id=obj)
        results = [x.probe for x in im_probe_query_set]
        cpm = models.CellProbeMap.objects.filter(probe_id__in=results)
        spm = models.StructureProbeMap.objects.filter(probe_id__in=results)
        cells = [x.cell for x in cpm]
        structures = [x.structure for x in spm]
        return cells, structures

    def get_cells(self, obj):
        final = CellSerializer(self.cellinstances, many=True).data
        return final

    def get_structures(self, obj):
        final = StructureSerializer(self.structureinstances, many=True).data
        return final





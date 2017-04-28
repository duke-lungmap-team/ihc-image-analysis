from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import  generics
from lungmap_sparql_client.lungmap_sparql_utils import *
from analytics.models import Experiment, ProbeExperiments, LungmapImage
from analytics import serializers
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
import django_filters

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

@api_view(['GET'])
def get_lung_map_experiments(request):
    """
    Utilizing the lungmap_sparql_client, calls out to the Lungmap mother ship 
    (via SPARQL) to get a list of all images, and associated data. From that point, 
    it de-duplicates experiment ids and provides a list to the user. 
    """
    exp_names_df = list_all_lungmap_experiments()
    return Response(exp_names_df)


class ExperimentList(generics.ListCreateAPIView):
    """
    List all experiments, or create a new experiment.
    """

    queryset = Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer


class ExperimentDetail(generics.RetrieveAPIView):
    """
    Get a single experiment
    """
    queryset = Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer
    lookup_field = 'experiment_id'


class ProbeDetail(APIView):
    def get_object(self, pk):
        try:
            return ProbeExperiments.objects.filter(experiment_id=pk)
        except ProbeExperiments.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        probes = self.get_object(pk)
        serializer = serializers.ProbeExperimentsSerializer(probes, many=True)
        return Response(serializer.data)


# noinspection PyClassHasNoInit
class LungmapImageFilter(django_filters.rest_framework.FilterSet):
     class Meta:
        model = LungmapImage
        fields = ['experiment']


class LungmapImageList(generics.ListAPIView):
    """
    List all images.
    """

    queryset = LungmapImage.objects.all()
    serializer_class = serializers.LungmapImageSerializer
    filter_class = LungmapImageFilter


class LungmapImageDetail(generics.RetrieveAPIView):
    """
    Get an image
    """

    queryset = LungmapImage.objects.all()
    serializer_class = serializers.LungmapImageSerializer


class ExperimentImageDetail(APIView):
    def get_object(self, pk):
        try:
            return LungmapImage.objects.filter(experiment_id=pk)
        except LungmapImage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        images = self.get_object(pk)
        serializer = serializers.LungmapImageSerializer(images, many=True)
        return Response(serializer.data)


class ImageJpeg(APIView):
    def get_object(self, ipk):
        try:
            return LungmapImage.objects.get(id=ipk).image_jpeg
        except LungmapImage.DoesNotExist:
            raise Http404

    def get(self, request, pk, ipk, format=None):
        jpeg = self.get_object(ipk)
        return HttpResponse(jpeg, content_type='image/jpeg')

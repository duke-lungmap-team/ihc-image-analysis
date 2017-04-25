
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins, generics
from lungmap_sparql_client.lungmap_sparql_utils import *
from analytics.models import Experiment, ProbeExperiments, LungmapImage
from analytics.serializers import (ExperimentSerializer,
                                   ProbeExperimentsSerializer, LungmapImageSerializer, UserSerializer)
from django.contrib.auth.models import User
from rest_framework import permissions

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LungmapExperimentViewSet(viewsets.ViewSet):
    """
    Utilizing the lungmap_sparql_client, this View calls out to the Lungmap mothership (via SPARQL) to get a list of all
    images, and associated data. From that point, it deduplicates experiment ids and provides a list to the user. 
    """
    permission_classes = (permissions.IsAdminUser,)
    def list(self, request):
        exp_names_df = list_all_lungmap_experiments()
        return Response(exp_names_df)

class ExperimentList(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    """
    List all experiments, or create a new experiment.
    """

    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ExperimentDetail(APIView):

    def get_object(self, pk):
        try:
            return Experiment.objects.get(pk=pk)
        except Experiment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        experiment = self.get_object(pk)
        serializer = ExperimentSerializer(experiment)
        return Response(serializer.data)

class ProbeDetail(APIView):
    def get_object(self, pk):
        try:
            return ProbeExperiments.objects.filter(experiment_id=pk)
        except ProbeExperiments.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        probes = self.get_object(pk)
        serializer = ProbeExperimentsSerializer(probes, many=True)
        return Response(serializer.data)

class ExperimentImageDetail(APIView):
    def get_object(self, pk):
        try:
            return LungmapImage.objects.filter(experiment_id=pk)
        except LungmapImage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        images = self.get_object(pk)
        serializer = LungmapImageSerializer(images, many=True)
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


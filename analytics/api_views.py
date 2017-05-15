from analytics import serializers, models
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from lungmap_sparql_client import lungmap_sparql_utils as sparql_utils
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
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
    exp_names_df = sparql_utils.list_all_lungmap_experiments()
    return Response(exp_names_df)


class ExperimentList(generics.ListCreateAPIView):
    """
    List all experiments, or create a new experiment.
    """

    queryset = models.Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer


class ExperimentDetail(generics.RetrieveAPIView):
    """
    Get a single experiment
    """
    queryset = models.Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer
    lookup_field = 'experiment_id'


class ProbeList(generics.ListAPIView):
    """
    List all probes
    """

    queryset = models.Probe.objects.all()
    serializer_class = serializers.ProbeSerializer


class ProbeDetail(generics.RetrieveAPIView):
    """
    Get a single probe
    """
    queryset = models.Probe.objects.all()
    serializer_class = serializers.ProbeSerializer


# noinspection PyClassHasNoInit
class LungmapImageFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = models.LungmapImage
        fields = ['experiment']


class LungmapImageList(generics.ListAPIView):
    """
    List all images.
    """

    queryset = models.LungmapImage.objects.all()
    serializer_class = serializers.LungmapImageSerializer
    filter_class = LungmapImageFilter


class LungmapImageDetail(generics.RetrieveAPIView):
    """
    Get an image
    """

    queryset = models.LungmapImage.objects.all()
    serializer_class = serializers.LungmapImageSerializer


@api_view(['GET'])
def get_image_jpeg(request, pk):
    """
    Get JPEG version of a single image
    :param request: HttpRequest
    :param pk: Primary key of an image
    :return: HttpResponse
    """
    image = get_object_or_404(models.LungmapImage, pk=pk)

    return HttpResponse(image.image_jpeg, content_type='image/jpeg')


# noinspection PyClassHasNoInit
class ExperimentProbeFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = models.ExperimentProbeMap
        fields = ['experiment']


class ExperimentProbeList(generics.ListAPIView):
    """
    List all experiment probes
    """

    queryset = models.ExperimentProbeMap.objects.all()
    serializer_class = serializers.ExperimentProbeSerializer
    filter_class = ExperimentProbeFilter


class ExperimentProbeDetail(generics.RetrieveAPIView):
    """
    Get an experiment probe
    """

    queryset = models.ExperimentProbeMap.objects.all()
    serializer_class = serializers.ExperimentProbeSerializer


from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins, generics
from lungmap_sparql_client.lungmap_sparql_utils import *
from analytics.models import Experiment, ProbeExperiments, LungmapImage
from analytics.serializers import (ExperimentSerializer, ExperimentIdSerializer,
                                   ProbeExperimentsSerializer, LungmapImageSerializer)



class LungmapExperimentViewSet(viewsets.ViewSet):
    """
    Utilizing the lungmap_sparql_client, this View calls out to the Lungmap mothership (via SPARQL) to get a list of all
    images, and associated data. From that point, it deduplicates experiment ids and provides a list to the user. 
    """
    def list(self, request):
        exp_names_df = list_all_lungmap_experiments()
        return Response(exp_names_df)


# class ExperimentList(APIView):
#
#     def get(self, request, format=None):
#         """
#         GET a list of all experiments loaded into the LAP system
#         """
#         experiments = Experiment.objects.all()
#         experiment = ExperimentIdSerializer(experiments, many=True)
#         return Response(experiment.data)
#
#     def post(self, request, format=None):
#         """
#         Load an experiment into the LAP system (admin users only)
#         """
#         serializer = ExperimentIdSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExperimentList(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    """
    List all experiments, or create a new experiment.
    """

    queryset = Experiment.objects.all()
    serializer_class = ExperimentIdSerializer

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

class ImageDetail(APIView):
    def get_object(self, pk):
        try:
            return LungmapImage.objects.filter(experiment_id=pk)
        except LungmapImage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        images = self.get_object(pk)
        serializer = LungmapImageSerializer(images, many=True)
        return Response(serializer.data)

# class ExperimentList(
#         mixins.ListModelMixin,
#         mixins.CreateModelMixin,
#         generics.GenericAPIView):
#     """
#     List all experiments, or create a new experiment.
#     """
#
#     queryset = Experiment.objects.all()
#     serializer_class = ExperimentSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class ExperimentList(APIView):
#     """
#     List all experiments, or create a new experiment.
#     """
#     def get_object(self, pk):
#         try:
#             return Experiment.objects.get(pk=pk)
#         except Experiment.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         experiment = self.get_object(pk)
#         serializer = ExperimentSerializer(experiment)
#         return Response(serializer.data)
#
#
# class ExperimentDetail(APIView):
#     """
#     Retrieve, update or delete an experiment instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Experiment.objects.get(pk=pk)
#         except Experiment.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         experiment = self.get_object(pk)
#         serializer = ExperimentSerializer(experiment)
#         return Response(serializer.data)

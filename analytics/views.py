from rest_framework import viewsets
import pandas as pd
from lungmap_sparql_client.lungmap_sparql_client import LMClient
from lungmap_sparql_client.lungmap_sparql_utils import get_lungmap_file_list_all
from analytics.models import Experiment
from analytics.serializers import ExperimentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics


class LungmapExperimentViewSet(viewsets.ViewSet):
    """
    Utilizing the lungmap_sparql_client, this View calls out to the Lungmap mothership (via SPARQL) to get a list of all
    images, and associated data. From that point, it deduplicates experiment ids and provides a list to the user. 
    """
    def list(self, request):
        alldata_df = pd.DataFrame(LMClient.create_image_table(get_lungmap_file_list_all))
        exp_names_df = alldata_df[['experiment_id']].drop_duplicates()
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
    """
    Retrieve, update or delete an experiment instance.
    """
    def get_object(self, pk):
        try:
            return Experiment.objects.get(pk=pk)
        except Experiment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        experiment = self.get_object(pk)
        serializer = ExperimentSerializer(experiment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ExperimentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from analytics import serializers, models
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from lungmap_client import lungmap_utils
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from tqdm import tqdm
import django_filters


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ImageSetList(generics.ListAPIView):
    queryset = models.ImageSet.objects.all()
    serializer_class = serializers.ImageSetSerializer


class ImageSetDetail(generics.RetrieveAPIView):
    """
    Get an image
    """

    queryset = models.ImageSet.objects.all()
    serializer_class = serializers.ImageSetDetailSerializer


class ExperimentList(generics.ListCreateAPIView):
    """
    List all experiments, or create a new experiment.
    """

    queryset = models.Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            with transaction.atomic():
                exp = models.Experiment(
                    experiment_id=data['experiment_id']
                )
                exp.save()

                images = lungmap_utils.get_images_by_experiment(exp.experiment_id)
                exp_probes = lungmap_utils.get_probes_by_experiment(exp.experiment_id)

                for exp_probe in tqdm(exp_probes):
                    probe, created = models.Probe.objects.get_or_create(
                        label=str.strip(exp_probe['probe_label'])
                    )

                    models.ExperimentProbeMap(
                        probe=probe,
                        color=str.strip(exp_probe['color']).lower(),
                        experiment_id=exp
                    ).save()

                for image in tqdm(images):
                    suf, sha1, suf_jpeg = lungmap_utils.get_image_from_s3(image['s3key'])
                    models.Image(
                        s3key=image['s3key'],
                        magnification=image['magnification'],
                        image_name=image['image_name'],
                        experiment=exp,
                        image_id=image['image_id'],
                        x_scaling=image['x_scaling'],
                        y_scaling=image['y_scaling'],
                        image_orig=suf,
                        image_orig_sha1=sha1,
                        image_jpeg=suf_jpeg
                    ).save()
        except Exception as e:  # catch any exception to rollback changes
            if hasattr(e, 'messages'):
                return Response(data={'detail': e.messages}, status=400)
            return Response(data={'detail': e.message}, status=400)

        serializer = serializers.ExperimentSerializer(
            exp,
            context={'request': request}
        )
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ImageDetailView(APIView):
    """
    A view to get specific image metadata and to post to cache images
    """
    def get(self, request, *args, **kwargs):
        img = get_object_or_404(models.Image, id=kwargs['pk'])
        serializer = serializers.ImageSerializer(img)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    def post(self, request, *args, **kwargs):
        img = get_object_or_404(models.Image, id=kwargs['pk'])
        suf, sha1, suf_jpeg = lungmap_utils.get_image_from_s3(img.s3key)
        img.image_orig = suf
        img.image_orig_sha1 = sha1
        img.image_jpeg = suf_jpeg
        img.save()
        serializer = serializers.ImageSerializer(img)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

@api_view(['GET'])
def get_image_jpeg(request, pk):
    """
    Get JPEG version of a single image
    :param request: HttpRequest
    :param pk: Primary key of an image
    :return: HttpResponse
    """
    image = get_object_or_404(models.Image, pk=pk)
    return HttpResponse(image.image_jpeg, content_type='image/jpeg')

# noinspection PyClassHasNoInit
class LungmapSubregionFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = models.Subregion
        fields = ['image']


class SubregionList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Subregion.objects.all()
    serializer_class = serializers.SubregionSerializer
    filter_class = LungmapSubregionFilter


class SubregionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Subregion.objects.all()
    serializer_class = serializers.SubregionSerializer


class ClassificationList(generics.ListAPIView):
    queryset = models.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer

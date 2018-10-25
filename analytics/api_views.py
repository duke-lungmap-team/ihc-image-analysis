from analytics import serializers, models
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from lungmap_client import lungmap_utils
from rest_framework import generics, permissions, status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from lung_map_utils import utils
import numpy as np
import pandas as pd
import hashlib
import os
from io import BytesIO
import pickle
# noinspection PyPackageRequirements
import cv2
# noinspection PyPackageRequirements
import PIL
import django_filters
# noinspection PyPackageRequirements
from sklearn.externals import joblib
import rest_framework.serializers as drf_serializers


# noinspection PyUnusedLocal
@api_view(['GET'])
def heartbeat(request):
    return Response()


# noinspection PyUnusedLocal
@api_view(['GET'])
def get_species_list(request):
    """
    Get list of distinct species labels
    """
    species = models.ImageSet.objects.order_by().values_list('species', flat=True).distinct()
    return Response(sorted(list(species)))


# noinspection PyUnusedLocal
@api_view(['GET'])
def get_magnification_list(request):
    """
    Get list of distinct magnification names
    """
    mags = models.ImageSet.objects.order_by().values_list('magnification', flat=True).distinct()
    return Response(sorted(list(mags)))


# noinspection PyUnusedLocal
@api_view(['GET'])
def get_development_stage_list(request):
    """
    Get list of distinct development stage names
    """
    dev_stages = models.ImageSet.objects.order_by().values_list(
        'development_stage',
        flat=True).distinct()
    return Response(sorted(list(dev_stages)))


class ProbeList(generics.ListAPIView):
    """
    List all probes
    """

    queryset = models.Probe.objects.all()
    serializer_class = serializers.ProbeSerializer


class OntoEntityRelationPartOf(generics.RetrieveAPIView):
    queryset = models.OntoEntity.objects.all()
    serializer_class = serializers.OntoEntitySerializer

    def serialize_relations(self, entity):
        data = self.get_serializer(entity).data
        data['relations'] = []
        relations = models.OntoEntityMap.objects.filter(has_part=entity)

        for r in relations:
            data['relations'].append(self.serialize_relations(r.entity))

        return data

    def retrieve(self, request, *args, **kwargs):
        entity = self.get_object()
        data = self.serialize_relations(entity)
        return Response(data)


# noinspection PyClassHasNoInit
class ImageSetFilter(django_filters.rest_framework.FilterSet):
    probe = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Probe.objects.all(),
        name='imagesetprobemap__probe'
    )

    class Meta:
        model = models.ImageSet
        fields = ['species', 'magnification', 'development_stage', 'probe']


class ImageSetList(generics.ListAPIView):
    queryset = models.ImageSet.objects.all()
    serializer_class = serializers.ImageSetSerializer
    filter_class = ImageSetFilter


class ImageSetDetail(generics.RetrieveAPIView):
    """
    Get an image set
    """

    queryset = models.ImageSet.objects.all()
    serializer_class = serializers.ImageSetSerializer


# noinspection PyClassHasNoInit
class ProbeOntoProteinMapFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = models.ProbeOntoProteinMap
        fields = ['probe', 'protein']


class ProbeProteinMapList(generics.ListAPIView):
    queryset = models.ProbeOntoProteinMap.objects.all()
    serializer_class = serializers.ProbeProteinMapSerializer
    filter_class = ProbeOntoProteinMapFilter


class ImageDetail(generics.RetrieveAPIView):
    """
    Get an image
    """

    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer_context = {
            'request': request
        }
        img = self.get_object()
        try:
            with transaction.atomic():
                if img.image_orig_sha1 is None or img.image_orig_sha1 == '':
                    file_name, tiff_data = lungmap_utils.get_image_from_lungmap(img.source_url)

                    with open(file_name[:-3], 'wb') as f3:
                        f3.write(tiff_data)

                        # noinspection PyUnresolvedReferences
                        cv_img = cv2.imread(f3.name)

                    os.remove(f3.name)

                    # noinspection PyUnresolvedReferences
                    pil_img = PIL.Image.fromarray(
                        cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB),
                        'RGB'
                    )
                    img_jpeg = pil_img.copy()
                    temp_handle = BytesIO()
                    pil_img.save(temp_handle, 'TIFF')
                    temp_handle.seek(0)

                    # jpeg image
                    temp_handle_jpeg = BytesIO()
                    img_jpeg.save(temp_handle_jpeg, 'JPEG')
                    temp_handle_jpeg.seek(0)

                    # filename
                    suf = SimpleUploadedFile(
                        file_name,
                        temp_handle.read(),
                        content_type='image/tif'
                    )
                    suf_jpg = SimpleUploadedFile(
                        file_name.replace('.tif', '.jpg'),
                        temp_handle_jpeg.read(),
                        content_type='image/jpeg'
                    )

                    temp_handle.seek(0)
                    image_orig_sha1 = hashlib.sha1(temp_handle.read()).hexdigest()

                    img.image_orig = suf
                    img.image_orig_sha1 = image_orig_sha1
                    img.image_jpeg = suf_jpg
                    img.save()
                serializer = serializers.ImageSerializer(
                    img,
                    context=serializer_context
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            if hasattr(e, 'messages'):
                return Response(data={'detail': e.messages}, status=400)
            return Response(data={'detail': e}, status=400)


# noinspection PyClassHasNoInit
class ImageFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = models.Image
        fields = ['experiment', 'image_set']


class ImageList(generics.ListAPIView):
    """
    List all images.
    """

    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_class = ImageFilter


class TrainedModelCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.TrainedModel.objects.all()
    serializer_class = serializers.TrainedModelCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            image_set = models.ImageSet.objects.get(id=request.data['imageset'])
            images = image_set.image_set.prefetch_related('subregion_set')
            training_data = []
            subregions = models.Subregion.objects.filter(image__image_set=image_set)\
                .values('entity__name') \
                .annotate(total=Count('entity__name')) \
                .order_by('entity__name')

            if len(subregions) <= 1:
                raise ValueError(
                    """
                    More than 1 anatomical structure is needed to train a model. Please 
                    continue to create training data by segmenting new anatomical structures. 
                    Once complete, a trained model can be created.
                    """
                )

            for sub in subregions:
                if sub['total'] < 4:
                    raise ValueError(
                        """
                        In order to train a model, we require that each imageset have 
                        at least 4 subregions for each anatomical structure. It seems 
                        that within this imageset, the anatomical structure %s has 
                        only %s subregion(s). Please either delete this subregion or 
                        continue to build training data for this structure.
                        """ % (sub['entity__name'], str(sub['total']))
                    )

            for image in images:
                sub_regions = image.subregion_set.all()

                if len(sub_regions) > 0:
                    # noinspection PyUnresolvedReferences
                    pil_image = PIL.Image.open(image.image_orig)
                    image_as_numpy = np.asarray(pil_image)

                    # noinspection PyUnresolvedReferences
                    sub_img = cv2.cvtColor(image_as_numpy, cv2.COLOR_RGB2HSV)

                    for subregion in sub_regions:
                        points = subregion.points.all()
                        this_mask = np.empty((0, 2), dtype='int')

                        for point in points:
                            this_mask = np.append(this_mask, [[point.x, point.y]], axis=0)

                        training_data.append(
                            utils.generate_features(
                                hsv_img_as_numpy=sub_img,
                                polygon_points=this_mask,
                                label=subregion.entity.name
                            )
                        )

            pipe = utils.pipeline
            training_data = pd.DataFrame(training_data)
            pipe.fit(training_data.drop('label', axis=1), training_data['label'])

            content = pickle.dumps(pipe)
            pickled_model = ContentFile(content)
            pickled_model.name = image_set.image_set_name + '.pkl'

            final = models.TrainedModel(imageset=image_set, model_object=pickled_model)
            final.save()

            return Response(
                serializers.TrainedModelSerializer(final).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:  # catch any exception to rollback changes
            if hasattr(e, 'messages'):
                return Response(data={'detail': e.messages}, status=400)

            return Response(data={'detail': str(e)}, status=400)


class TrainedModelDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a trained model
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.TrainedModel.objects.all()
    serializer_class = serializers.TrainedModelSerializer


# noinspection PyUnusedLocal
@api_view(['GET'])
def get_image_jpeg(request, pk):
    """
    Get JPEG version of a single image
    """
    image = get_object_or_404(models.Image, pk=pk)
    if image.image_jpeg.name == '':
        content = {'image_jpeg': 'image not yet cached'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        return HttpResponse(image.image_jpeg, content_type='image/jpeg')


class ClassifySubRegion(generics.CreateAPIView):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ClassifyPointsSerializer

    # noinspection PyMethodMayBeStatic
    def create(self, request, *args, **kwargs):
        image_id = request.data['image_id']
        points = request.data['points']
        image_object = models.Image.objects.get(id=image_id)
        image_set = models.ImageSet.objects.get(id=image_object.image_set_id)
        this_model = joblib.load(image_set.trainedmodel.model_object)
        this_mask = np.empty((0, 2), dtype='int')

        for point in points:
            this_mask = np.append(this_mask, [[point['x'], point['y']]], axis=0)
        # noinspection PyUnresolvedReferences
        pil_image = PIL.Image.open(image_object.image_orig)
        image_as_numpy = np.asarray(pil_image)

        # noinspection PyUnresolvedReferences
        image_as_numpy = cv2.cvtColor(image_as_numpy, cv2.COLOR_RGB2HSV)
        features = utils.generate_features(
            hsv_img_as_numpy=image_as_numpy,
            polygon_points=this_mask
        )
        features_data_frame = pd.DataFrame([features])
        model_classes = list(this_model.named_steps['classification'].classes_)
        probabilities = this_model.predict_proba(features_data_frame.drop('label', axis=1))

        assert (len(model_classes) == probabilities.shape[1])

        results = {"results": []}
        results['results'].extend(
            [{a: probabilities[0][i]} for i, a in enumerate(model_classes)]
        )

        return Response(results, status=status.HTTP_200_OK)


# noinspection PyClassHasNoInit
class LungmapSubRegionFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = models.Subregion
        fields = ['image', 'entity']


class SubregionList(
        mixins.DestroyModelMixin,
        generics.ListCreateAPIView
):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Subregion.objects.all()
    serializer_class = serializers.SubregionSerializer
    filter_class = LungmapSubRegionFilter

    def create(self, request, *args, **kwargs):
        """
        A bit of a special case with this API endpoint. We don't allow the creation of
        new sub-regions for a image / entity class combination if there are existing
        sub-regions for that pair. So, a POST will take a list of sub-regions and check
        that none exist before saving them in bulk within an atomic transaction.

        The save will also fail if there are a mixture of different image or entity IDs,
        all sub-regions in the list must have the same image ID and entity ID.
        """

        # A couple checks to make sure we can continue...
        # First, if the image set for the image is already trained, we do not allow
        # new sub-regions.
        # Second, as of now, we don't allow new sub-regions for an image / entity combo if
        # existing sub-regions exist for it. This may change in the future.
        # Third, we don't allow a bulk POST with a different image / entity combos. Since
        # we will have the first region image / entity combo from the previous check,
        # we can verify that all the rest are the same as we iterate through them.
        image_id = request.data[0]['image']

        # get image set to check if it is trained already
        image = models.Image.objects.get(id=image_id)
        image_set = models.ImageSet.objects.get(id=image.image_set_id)

        if hasattr(image_set, 'trainedmodel'):
            return Response(data={'detail': "Image set is already trained"}, status=400)

        entity_id = request.data[0]['entity']
        existing_sub_regions = models.Subregion.objects.filter(
            image=image_id,
            entity=entity_id
        )

        if existing_sub_regions.count() > 0:
            raise drf_serializers.ValidationError(
                "Sub-regions already exist for this image / entity"
            )

        sub_regions = []

        try:
            with transaction.atomic():
                for r in request.data:
                    if image_id != r['image']:
                        raise drf_serializers.ValidationError(
                            "All sub-regions must reference the same image"
                        )

                    if entity_id != r['entity']:
                        raise drf_serializers.ValidationError(
                            "All sub-regions must reference the same entity class"
                        )

                    subregion = models.Subregion.objects.create(
                        image_id=image_id,
                        entity_id=entity_id,
                        user_id=request.user.id
                    )

                    for p in r['points']:
                        models.Points.objects.create(
                            subregion=subregion,
                            x=p['x'],
                            y=p['y'],
                            order=p['order']
                        )

                    sub_regions.append(subregion)
        except Exception as e:  # catch any exception to rollback changes
            # noinspection PyUnresolvedReferences
            return Response(data={'detail': e.message}, status=400)

        serializer = serializers.SubregionSerializer(
            sub_regions,
            context={'request': request},
            many=True
        )
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    # noinspection PyMethodMayBeStatic
    def delete(self, request):
        # Allow deleting sub-regions in bulk given query parameters for
        # both the Image and Anatomy IDs. However, deleting sub-regions
        # for image sets with a trained model is not allowed.
        try:
            entity_id = request.query_params['entity']
            image_id = request.query_params['image']
        except KeyError:
            return Response(
                data={'detail': "Anatomy and Image must be specified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(
                data={'detail': "Image ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if related image set is already trained
        trained_models = models.TrainedModel.objects.filter(imageset=image.image_set_id)

        if trained_models.count() > 0:
            return Response(
                data={'detail': "Sub-regions for trained image sets cannot be deleted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        regions = models.Subregion.objects.filter(entity=entity_id, image=image_id)
        regions.delete()

        response_data = {'success': True}

        return Response(response_data, status=status.HTTP_200_OK)


class SubregionDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Subregion.objects.all()
    serializer_class = serializers.SubregionSerializer

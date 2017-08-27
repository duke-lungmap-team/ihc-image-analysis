from django.conf.urls import url
from analytics import api_views


urlpatterns = [
    url(r'^api/species/$', api_views.get_species_list, name='species-list'),
    url(r'^api/magnifications/$', api_views.get_magnification_list, name='magnification-list'),
    url(r'^api/images/$', api_views.ImageList.as_view()),
    url(r'^api/images/(?P<pk>[0-9]+)/$', api_views.ImageDetail.as_view()),
    url(r'^api/images-jpeg/(?P<pk>[0-9]+)/$', api_views.get_image_jpeg, name='image-jpeg'),
    url(r'^api/users/$', api_views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', api_views.UserDetail.as_view()),
    url(r'^api/subregion/$', api_views.SubregionList.as_view()),
    url(r'^api/subregion/(?P<pk>[0-9]+)/$', api_views.SubregionDetail.as_view()),
    url(r'^api/subregion-anatomy-count/$', api_views.SubregionAnatomyAggregation.as_view()),
    url(r'^api/image-sets/$', api_views.ImageSetList.as_view()),
    url(r'^api/image-sets/(?P<pk>[0-9]+)/$', api_views.ImageSetDetail.as_view()),
    url(r'^api/anatomy/(?P<pk>[0-9]+)/$', api_views.AnatomyList.as_view()),
    url(r'^api/anatomybyprobe/(?P<pk>[0-9]+)/$', api_views.AnatomyByProbeList.as_view()),
    url(r'^api/train-model/$', api_views.TrainedModelCreate.as_view()),
    url(r'^api/classify/$', api_views.ClassifySubRegion.as_view())
]

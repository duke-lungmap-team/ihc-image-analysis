from django.conf.urls import url
from analytics import api_views


urlpatterns = [
    url(r'^api/lungmapexperiments/', api_views.get_lung_map_experiments),
    url(r'^api/experiments/$', api_views.ExperimentList.as_view()),
    url(r'^api/experiments/(?P<experiment_id>[\w{}.-]{1,14})/$', api_views.ExperimentDetail.as_view()),
    url(r'^api/images/$', api_views.LungmapImageList.as_view()),
    url(r'^api/images/(?P<pk>[0-9]+)/$', api_views.LungmapImageDetail.as_view()),
    url(r'^api/images-jpeg/(?P<pk>[0-9]+)/$', api_views.get_image_jpeg, name='image-jpeg'),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/probes/$', api_views.ExperimentProbeDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/images/$', api_views.ExperimentImageDetail.as_view()),
    url(r'^api/users/$', api_views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', api_views.UserDetail.as_view()),
]

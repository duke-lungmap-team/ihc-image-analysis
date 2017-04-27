from django.conf.urls import url
from analytics import api_views


urlpatterns = [
    url(r'^api/lungmapexperiments/', api_views.LungmapExperimentViewSet.as_view({'get': 'get_lm_experiments'})),
    url(r'^api/experiments/$', api_views.ExperimentList.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/$', api_views.ExperimentDetail.as_view()),
    url(r'^api/images/$', api_views.LungmapImageList.as_view()),
    url(r'^api/images/(?P<pk>[0-9]+)/$', api_views.LungmapImageDetail.as_view()),
    url(r'^api/images/(?P<pk>[0-9]+)/jpeg/$', api_views.ImageJpeg.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/probes/$', api_views.ProbeDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/images/$', api_views.ExperimentImageDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/images/(?P<ipk>[0-9]+)/$', api_views.ImageJpeg.as_view()),
    url(r'^api/users/$', api_views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', api_views.UserDetail.as_view()),
]

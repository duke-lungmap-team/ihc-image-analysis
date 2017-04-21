"""lap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from analytics import api_views


urlpatterns = [
    url(r'^api/lungmapexperiments/', api_views.LungmapExperimentViewSet.as_view({'get': 'get_lm_experiments'})),
    url(r'^api/experiments/$', api_views.ExperimentList.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/$', api_views.ExperimentDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/probes/$', api_views.ProbeDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/images/$', api_views.ExperimentImageDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/images/(?P<ipk>[0-9]+)/$', api_views.ImageJpeg.as_view()),
    url(r'^api/users/$', api_views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', api_views.UserDetail.as_view()),
]

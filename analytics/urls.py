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
from rest_framework.urlpatterns import format_suffix_patterns
from analytics.views import (LungmapExperimentViewSet, ExperimentList, ExperimentDetail,
                             ProbeDetail, ImageDetail)


urlpatterns = [
    url(r'^api/lungmapexperiments/', LungmapExperimentViewSet.as_view({'get': 'list'}), name='lungmapexperiments'),
    url(r'^api/experiments/$', ExperimentList.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,40})/$', ExperimentDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/probes/$', ProbeDetail.as_view()),
    url(r'^api/experiments/(?P<pk>[\w{}.-]{1,14})/images/$', ImageDetail.as_view()),
]


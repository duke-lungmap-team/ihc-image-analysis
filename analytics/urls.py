from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import  static

from analytics import api_views


urlpatterns = [
    url(r'^api/images/$', api_views.LungmapImageList.as_view()),
    url(r'^api/images/(?P<pk>[0-9]+)/$', api_views.LungmapImageDetail.as_view()),
    url(r'^api/images-jpeg/(?P<pk>[0-9]+)/$', api_views.get_image_jpeg, name='image-jpeg'),
    url(r'^api/users/$', api_views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', api_views.UserDetail.as_view()),
    url(r'^api/subregion/$', api_views.SubregionList.as_view()),
    url(r'^api/subregion/(?P<pk>[0-9]+)/$', api_views.SubregionDetail.as_view()),
    url(r'^api/classifications/$', api_views.ClassificationList.as_view()),
    url(r'^api/imagesets/$', api_views.ImageSetList.as_view()),
    url(r'^api/imagesets/(?P<pk>[0-9]+)/$', api_views.ImageSetDetail.as_view()),

]

#TODO: this is a no-no, but not sure how else to serve it, ng-src is calling /media not /api
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
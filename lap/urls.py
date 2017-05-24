from django.conf.urls import url, include
from django.contrib import admin
from analytics import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('authenticate.urls')),
    url(r'^', include('analytics.urls')),
    url(r'^docs/', schema_view),
    url(r'^$', views.ihc_app, name='home')
]

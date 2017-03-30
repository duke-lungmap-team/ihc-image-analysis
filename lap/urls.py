from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('analytics.urls')),
    url(r'^docs/', include_docs_urls(title='Lungmap Analytic Platform')),
]

from django.conf.urls import url
from authenticate import views

__author__ = 'swhite'

urlpatterns = [
    url(r'^login/?$', views.login_view, name="login"),
    url(r'^logout/?$', views.logout_view, name="logout"),
    url(r'^login_failed/?$', views.login_failed, name="login_failed"),
]

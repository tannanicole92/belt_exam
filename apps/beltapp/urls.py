from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^exists$', views.exists),
    url(r'^create$', views.create),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^add_trip$', views.add_trip),
    url(r'^travels/(?P<id>\d+)/join$', views.join),
]

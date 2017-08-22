from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^exists$', views.exists),
    url(r'^create$', views.create),
    url(r'^travels$', views.travels),
    url(r'^portfolio/(?P<user_id>\d+)$', views.portfolio),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^deletetrip/(?P<id>\d+)/(?P<user_id>\d+)$', views.deletetrip),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^add_trip$', views.add_trip),
    url(r'^travels/(?P<id>\d+)/join$', views.join),
    url(r'^travels/(?P<id>\d+)/(?P<user_id>\d+)/joining$', views.joining),
    url(r'^travels/(?P<id>\d+)/(?P<user_id>\d+)/leaving$', views.leaving),
    url(r'^travels/(?P<id>\d+)/(?P<user_id>\d+)/joiners$', views.joiners),
    url(r'^travels/(?P<id>\d+)/(?P<user_id>\d+)/leaves$', views.leaves),

]

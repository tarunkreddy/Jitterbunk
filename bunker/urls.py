from django.conf.urls import url

from . import views

app_name = 'bunker'
urlpatterns = [
    url(r'^$', views.display_index, name='index'),
    url(r'^(?P<page_id>[0-9]*)/$', views.display_index, name='index'),
    url(r'^profile/(?P<pk>\w+)/$', views.PersonalView.as_view(), name='personal'),
    url(r'^(?P<user_id>[0-9]+)/send-bunk/$', views.send_bunk, name='send-bunk'),
    url(r'^stats/(?P<user_id>\w*)/$', views.get_stats, name='get-stats'),


]

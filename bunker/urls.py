from django.conf.urls import url

from . import views

app_name = 'bunker'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\w+)/$', views.PersonalView.as_view(), name='personal'),
    url(r'^(?P<user_id>[0-9]+)/send-bunk/$', views.send_bunk, name='send-bunk'),
    url(r'^bunk-submitted/$', views.bunk_submitted, name='bunk-submitted'),

]

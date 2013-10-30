from django.conf.urls import patterns, url
from clock import views

urlpatterns = patterns('',
    url(r'^$', views.Punches.as_view(), name='index'), 
	url(r'^addNote/(?P<pk>\d+)/$', views.AddNote.as_view(), name='add-note'),
    url(r'^record/add/$', views.RecordAdd.as_view(), name='clock-in'),
    url(r'^clockOut/(?P<rec_id>\d+)/$', views.clockOut, name='clock-out'),
#    url(r'^record/(?P<pk>\d+)/$', views.RecordDetail.as_view(), name='record-detail'),
    url(r'^record/(?P<pk>\d+)/edit/$', views.RecordUpdate.as_view(), name='record-update'),
#    url(r'^record/(?P<pk>\d+)/delete/$', views.RecordDelete.as_view(), name='record-delete'),
)

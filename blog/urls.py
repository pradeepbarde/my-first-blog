from django.urls import path
# import url
from django.conf.urls import url
from . import views
urlpatterns = [
    # home page
    path('', views.index, name='index'),

    # Topics Page
    path('Topics/', views.topics, name='topics'),

    # Detail page for a single topic

    url(r'^Topics/(?P<topic_id>\d+)/$', views.topic, name='topic'), 

    # Page for adding a new topic
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    # Page for adding a new entry       #<------------->
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # Page for editing an entry
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

    # Page for adding a download  <--------
    url(r'^(?P<fileupload_id>\d+)/download_file/$', views.download_file, name='download_file'),

    
]
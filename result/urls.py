from django.conf.urls import url
from . import views
from .import forms
urlpatterns = [
    
    url(r'^hi/$', views.result_list, name='result_list'),
    url(r'^login/$', views.result_login, name='result_login'),
    #url(r'^new/$',forms.ResultCreateView, name='result_create'),
]
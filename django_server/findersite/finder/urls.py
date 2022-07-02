from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'finder'
urlpatterns = [
            url(r'^$', views.SearchFormView.as_view(), name='search'),
            url(r'^result/$', views.IndexView.as_view(), name='result'),
            ]

from django.urls import path

from . import views

app_name = 'finder'
urlpatterns = [
            path('', views.SearchFormView.as_view(), name='search'),
            ]

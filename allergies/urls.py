from django.urls import path

from . import views

app_name = 'allergies'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('request/', views.ask, name='request'),
    path('contact/', views.contact, name='contact'),
]
from django.urls import path, re_path

from . import views

app_name = 'allergies'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('request/', views.ask, name='request'),
    path('contact/', views.contact, name='contact'),
    path('lookup/', views.lookup, name='lookup'),
    path('check/<str:st>', views.check, name='check'),
]
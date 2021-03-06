from django.urls import path, re_path

from . import views

app_name = 'allergies'
urlpatterns = [
    path('', views.search, name='index'),
    path('request/', views.ask, name='request'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('get_names/', views.get_restaurant, name='get_names'),
]

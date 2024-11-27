from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('fighter/<int:fighter_id>/', views.fighter_profile, name='fighter_profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

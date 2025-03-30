from django.urls import path
from . import views

app_name = 'users'  # This helps with URL namespacing

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('registration/', views.registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    path('events/', views.events, name='events'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contactus, name='contact'),
]
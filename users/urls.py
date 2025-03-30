from django.urls import path
from . import views

app_name = 'users'  # This helps with URL namespacing

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('registration/', views.registration, name='registration'),
    path('registration2/', views.registration2, name='registration2'),
    path('blog/', views.blog, name='blog'),
    path('events/', views.events, name='events'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),
    path('coursedetail1/', views.coursedetail1, name='coursedetail1'),
    path('coursedetail2/', views.coursedetail2, name='coursedetail2'),
    path('coursedetail3/', views.coursedetail3, name='coursedetail3'),
    path('coursedetail4/', views.coursedetail4, name='coursedetail4'),
    path('coursedetail5/', views.coursedetail5, name='coursedetail5'),
    path('coursedetail6/', views.coursedetail6, name='coursedetail6'),
]

from django.urls import path
from blogApp import views

app_name = 'blogApp'

urlpatterns = [
    path('', views.blogList, name="blog-list"),
    path('category/<slug>/', views.category_detail, name="category_detail"),
    path('<pid>', views.blogDetail, name="blog-detail"),

]

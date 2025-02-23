from django.urls import path
from . import views 

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('search/', views.search_by_name, name='search_by_name'),
    path('calculate_averages/', views.calculate_averages, name='calculate_averages'),
]
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('', views.csv_import_list, name='csv_list'),
    path('post/<int:pk>/', views.csv_import_detail, name='csv_import'),
    path('post/new/', views.csv_import_new, name='csv_new'),
]
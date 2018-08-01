from django.urls import path
from . import views


urlpatterns = [
    path('saveLineItem/', views.saveLineItem, name='saveLineItem'),
    path('', views.addForm, name='addForm'),
]

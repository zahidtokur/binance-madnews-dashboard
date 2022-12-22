from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
]
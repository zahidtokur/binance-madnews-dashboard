from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('<int:id>/set-main/', views.SetMainAccountView.as_view(), name='set_main'),
]
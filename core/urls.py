from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('list/', views.AccountListView.as_view(), name='list'),
    path('<int:id>/update/', views.AccountUpdateView.as_view(), name='update'),
    path('<int:id>/delete/', views.AccountDeleteView.as_view(), name='delete'),
    path('<int:id>/set-main/', views.SetMainAccountView.as_view(), name='set_main'),
]
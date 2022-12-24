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
    path('update-balance/', views.UpdateBalanceView.as_view(), name='update_balance'),
    path('get-pairs/', views.GetPairsView.as_view(), name='get_pairs'),
    path('set-cross-margin/', views.SetCrossMarginView.as_view(), name='set_cross_margin'),
    path('set-leverage/', views.SetLeverageView.as_view(), name='set_leverage'),
]
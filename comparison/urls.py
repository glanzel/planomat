from django.urls import path
from . import views

app_name = 'comparison'

urlpatterns = [
    path('', views.poll, name='start_poll'),
    path('economics/', views.EconomicListView.as_view(), name='economic_list'),
    path('compare/', views.compare_view, name='compare'),
    path('results/', views.results_view, name='results'),
    path('poll/<int:nr>/', views.poll, name='poll'),
    path('save_poll/<int:nr>/', views.save_poll, name='save_poll'),
]

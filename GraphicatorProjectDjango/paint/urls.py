from django.urls import path
from . import views

app_name = 'paint'

urlpatterns = [
    path('', views.paint_view, name='paint'),
    path('documentation/', views.documentation_view, name='documentation'),
]
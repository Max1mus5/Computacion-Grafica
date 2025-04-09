from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('editor/', views.editor, name='editor'),
    path('process-image/', views.process_image, name='process_image'),
    path('generate-histogram/', views.generate_histogram, name='generate_histogram'),
]
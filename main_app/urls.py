from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('pens/', views.pen_index, name='pen-index'),
  path('pens/<int:pen_id>/', views.pen_detail, name='pen-detail'),
]
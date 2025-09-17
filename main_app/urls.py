from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('pens/', views.pen_index, name='pen-index'),
  path('pens/<int:pen_id>/', views.pen_detail, name='pen-detail'),
  path('pens/create/', views.PenCreate.as_view(), name='pen-create'),
  path('pens/<int:pk>/update/', views.PenUpdate.as_view(), name='pen-update'),
  path('pens/<int:pk>/delete/', views.PenDelete.as_view(), name='pen-delete'),
  path('inks/create/', views.InkCreate.as_view(), name='ink-create'),
  path('inks/<int:ink_id>/', views.ink_detail, name='ink-detail'),
  path('inks/', views.InkList.as_view(), name='ink-index'),
  path('pens/<int:pen_id>/associate-ink/<int:ink_id>/', views.associate_ink, name='associate-ink'),
  path('pens/<int:pen_id>/remove-ink/<int:ink_id>/', views.remove_ink, name='remove-ink'),
  path('accounts/signup/', views.signup, name='signup'),
]
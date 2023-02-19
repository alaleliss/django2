from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('post/<slug>/', views.post_detail, name='post_detail'),
    path('post_create/', views.post_create, name='post_create'),
    path('post_delete/<slug>', views.post_delete, name='post_delete'),
    path('post_edit/<slug>', views.post_edit, name='post_edit'),
    path('<slug>/like', views.like, name='like'),
    path('<slug>/dislike', views.dislike, name='dislike'),
    path('<int:pk>/delete', views.delete_comment, name='delete_comment'),
    path('<int:pk>/edit', views.edit_comment, name='edit_comment')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('search/', views.blog_search, name='blog_search'),
    path('<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tagged_posts, name='tagged_posts'),
    # Remove the add_comment path
]
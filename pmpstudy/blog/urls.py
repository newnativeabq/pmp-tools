"""blog application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<slug:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/edit/<slug:pk>/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/delete/<slug:pk>/', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts/', views.DraftListView.as_view(), name='drafts'),
    path('comment/post<slug:pk>/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<slug:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<slug:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('post/publish/<slug:pk>/', views.post_publish, name='post_publish')
]
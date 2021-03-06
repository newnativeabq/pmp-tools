"""pmpstudy URL Configuration

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
from django.urls import include

from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

import flashcard.views as card_views

urlpatterns = [
    path('', TemplateView.as_view(template_name="sitenav/index.html"), name='home'),
    path('flashcards/', include(('flashcard.urls', 'flashcards'), namespace='flashcards')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('admin/', admin.site.urls),
]

"""flachard application URL Configuration

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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.FlashCardHomeView.as_view(), name="card_home"),
    path('card/list', views.CardListView.as_view(), name='card_list'),
    path('card/<slug:pk>', views.CardDetailView.as_view(), name='card_detail'),
    path('card/new/', views.CardCreateView.as_view(), name='card_create'),
    path('card/<slug:pk>/edit', views.CardUpdateView.as_view(), name='card_update'),
    path('card/<slug:pk>/delete', views.CardDeleteView.as_view(), name='card_delete'),
    path('card/launch/', views.CardShowView.as_view(), name='card_launch'),
    path('drafts', views.CardDraftList.as_view(), name='card_drafts'),
    path('card/activate/<slug:pk>/', views.activateCardView, name='card_activate'),
    path('card/deactivate/<slug:pk>/', views.deactivateCardView, name='card_deactivate'),
]
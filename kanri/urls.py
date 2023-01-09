from django.urls import path
from django.contrib.auth import views
from .views import (CommunityListViewSet
)

urlpatterns = [
    path('api/community/', CommunityListViewSet.as_view({
        'get': 'getall',
    })),
    path('api/community/<str:slug>/', CommunityListViewSet.as_view({
        'get': 'retrieve',
    })),
]
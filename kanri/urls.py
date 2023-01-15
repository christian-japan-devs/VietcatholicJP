from django.urls import path
from django.contrib.auth import views
from .views import (CommunityListViewSet,ContactViewSet,ContactUpdateViewSet
)

urlpatterns = [
    path('api/community/', CommunityListViewSet.as_view({
        'get': 'getall',
    })),
    path('api/community/<str:slug>/', CommunityListViewSet.as_view({
        'get': 'retrieve',
    })),
    path('api/contact-us/create', ContactViewSet.as_view({
        'post': 'create',
    })),
    path('api/contact-us/update/', ContactUpdateViewSet.as_view({
        'post': 'update',
    })),

]
from django.urls import path
from django.contrib.auth import views
from .views import (CommunityListViewSet,ContactViewSet,ContactUpdateViewSet
            ,ChurchViewSet,FatherViewSet
)

urlpatterns = [
    path('api/community/', CommunityListViewSet.as_view({
        'get': 'getall',
    })),
    path('api/community/search/', CommunityListViewSet.as_view({
        'get': 'search',
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
    path('api/church/', ChurchViewSet.as_view({
        'get': 'get_all',
    })),
    path('api/church/<int:id>/', ChurchViewSet.as_view({
        'get': 'retrieve',
    })),
    path('api/father/', FatherViewSet.as_view({
        'get': 'get_all',
    })),
    path('api/father/<int:id>/', FatherViewSet.as_view({
        'get': 'retrieve',
    })),

]
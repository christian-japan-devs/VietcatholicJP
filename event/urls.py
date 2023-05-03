from django.urls import path
from django.contrib.auth import views
from .views import (RegistrationListViewSet,RegistrationAdminViewSet
)

urlpatterns = [
    path('api/event/youthday/get-ticket', RegistrationListViewSet.as_view({
        'get': 'getall',
    })),
    path('api/event/youthday/add-ticket', RegistrationAdminViewSet.as_view({
        'post': 'create',
    })),
    path('api/event/youthday/update-ticket', RegistrationAdminViewSet.as_view({
        'post': 'update',
    })),
    path('api/event/youthday/checkin-ticket', RegistrationAdminViewSet.as_view({
        'get': 'checkin',
    })),
]

from django.urls import path
from .views import (
    UserCreate, GoogleLoginView
)

urlpatterns = [
    path('account/create', UserCreate.as_view({
        'post': 'create',
    })),
    path('account/confirm', UserCreate.as_view({
        'post': 'confirm',
    })),
    path('account/request-password', UserCreate.as_view({
        'post': 'requestPassword',
    })),
    path('account/reset-password', UserCreate.as_view({
        'post': 'resetPassword',
    })),
    path('social/login/google/', GoogleLoginView.as_view(), name = "google"),
]
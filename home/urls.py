from django.urls import path
from django.contrib.auth import views
from .views import (home,UserLoginForm)
from .api import (LetterListViewSet, MassScheduleViewSet, 
    AnnouncementListViewSet,VideoLinksListViewSet,
    PostListViewSet
)

urlpatterns = [
    path('', views.LoginView.as_view(template_name='main/home.html',authentication_form=UserLoginForm), name='vietcatholic-home'),
    path('api/letter/', LetterListViewSet.as_view({
        'get': 'getfirstletter',
    })),
    path('api/letter/<str:slug>/', LetterListViewSet.as_view({
        'get': 'retrieve'
    })),
    path('api/massschedule/', MassScheduleViewSet.as_view({
        'get': 'get_nearest_mass_schedule',
    })),
    path('api/announcement/', AnnouncementListViewSet.as_view({
        'get': 'getannouncements',
    })),
    path('api/announcement/<str:slug>/', AnnouncementListViewSet.as_view({
        'get': 'retrieve'
    })),
    path('api/videolinks/', VideoLinksListViewSet.as_view({
        'get': 'getVideoLinks',
    })),
    path('api/post/gettype/', PostListViewSet.as_view({
        'get': 'gettypes',
    })),
    path('api/post/', PostListViewSet.as_view({
        'get': 'getposts',
    })),
]
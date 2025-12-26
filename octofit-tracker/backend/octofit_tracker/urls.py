"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from . import views
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'leaderboard', views.LeaderboardViewSet)
router.register(r'workouts', views.WorkoutViewSet)

@api_view(['GET'])
def api_root(request, format=None):
    """Return API root using Codespace hostname when available.

    If the environment variable CODESPACE_NAME is set we construct the
    canonical API URLs using the Codespaces app hostname:
    https://$CODESPACE_NAME-8000.app.github.dev/api/<component>/

    Fallback: use request.build_absolute_uri() when CODESPACE_NAME is not set.
    """
    codespace = os.environ.get('CODESPACE_NAME')
    if codespace:
        codespace = codespace.strip()
        if codespace:
            base = f"https://{codespace}-8000.app.github.dev/api/"
        else:
            base = None
    else:
        base = None
    if base:
        return Response({
            'users': base + 'users/',
            'teams': base + 'teams/',
            'activities': base + 'activities/',
            'leaderboard': base + 'leaderboard/',
            'workouts': base + 'workouts/',
        })

    return Response({
        'users': request.build_absolute_uri('users/'),
        'teams': request.build_absolute_uri('teams/'),
        'activities': request.build_absolute_uri('activities/'),
        'leaderboard': request.build_absolute_uri('leaderboard/'),
        'workouts': request.build_absolute_uri('workouts/'),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', api_root, name='api-root'),
]

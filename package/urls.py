from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cms-home'),
    path('team/', views.team, name='cms-team'),
    path('project/', views.project, name='cms-project'),
    path('signup/', views.signup, name='cms-signup'),
    path('track/', views.track, name='cms-track'),
    path('ship/', views.ship, name='cms-ship'),
]
"""talenthub URL Configuration

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from talenthub import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("profile/<username>/", views.profile, name="profile"),
    path("myProfile/", views.myProfile, name="myProfile"),
    path("myOffers/", views.myOffers, name="myOffers"),
    path("myMeetings/", views.myMeetings, name="myMeetings"),
    path("addOffer/", views.addOffer, name="addOffer"),
    path("addMeeting/<int:offer_id>", views.addMeeting, name="addMeeting"),
    path("addOpinion/", views.addOpinion, name="addOpinion"),
]

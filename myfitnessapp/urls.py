"""
URL configuration for myfitnessapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from workouts.views import login_view, logout_view, register_view, index_view, profile_view, update_entry, create_week, profile_redirect

urlpatterns = [
    path('', index_view, name='home'),  # default homepage
    path('admin/', admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("index/", index_view, name="index"),
    path("profile_redirect/", profile_redirect, name="profile_redirect"),
    path("profile/", profile_view, name="profile"),
    path("update_entry/", update_entry, name="update_entry"),
    path("create_week/", create_week, name="create_week"),



]



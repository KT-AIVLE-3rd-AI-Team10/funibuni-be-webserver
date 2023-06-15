"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from accounts.views import user_register_view, user_login_view, user_logout_view, user_update_view, user_delete_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/register/', user_register_view, name='user-register'),
    path('api/login/', user_login_view, name='user-login'),
    path('api/logout/', user_logout_view, name='user-logout'),
    path('api/update/', user_update_view, name='user-update'),
    path('api/delete/', user_delete_view, name='user-delete'),
]
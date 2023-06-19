"""
URL configuration for bigproject project.

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
from accounts.views import user_signup_view, phone_number_login,user_logout_view,user_delete_view,user_info_view
from post.views import get_post_list,create_post,post_detail
from reports.views import report_post
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/user/signup', user_signup_view, name='user_signup'),
    path('api/user/signin', phone_number_login, name='phone_number_login'),
    path('api/user/signout', user_logout_view, name='user_signout'),
    path('api/user/withdrawal', user_delete_view, name='user-withdrawal'),
    path('api/user/info', user_info_view, name='user-info'),
    
    path('api/posts', get_post_list, name='post-list'),
    path('api/posts/create', create_post, name='post-create'),
    path('api/posts/<int:pk>', post_detail, name='post-detail'),
    path('api/posts/<int:post_id>/report', report_post, name='report_post'),
    
    
]
    

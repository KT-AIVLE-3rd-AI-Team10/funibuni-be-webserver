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
from accounts.views import user_register_view, user_login_view, user_logout_view, user_delete_view,user_info_view
from post.views import get_post_list, get_post_detail, create_post, update_post, delete_post

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/user/signup', user_register_view, name='user-signup'),
    path('api/user/signin', user_login_view, name='user-signin'),
    path('api/user/singout', user_logout_view, name='user-singout'),
    path('api/user/info', user_info_view, name='user-info'),
    path('api/user/withdrawal', user_delete_view, name='user-withdrawal'),
    path('api/user/info', user_info_view, name='user-info'),
    #게시판
    path('post/', get_post_list, name='post-list'),
    path('post/<int:post_id>/', get_post_detail, name='post-detail'),
    path('post/create/', create_post, name='post-create'),
    path('post/<int:post_id>/update/', update_post, name='post-update'),
    path('post/<int:post_id>/delete/', delete_post, name='post-delete'),
    #댓글
    
]
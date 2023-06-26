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
from accounts.views import user_signup_view, phone_number_login, user_logout_view, user_delete_view, user_info_view,auto_signin,token_refresh
from post.views import create_post,post_detail,post_list,update_sharing,create_postreport,post_like,comment_create,comment_detail,comment_report,create_reply,reply_detail,reply_report
from waste.views import image_upload#, waste_apply
from myburni.views import sharing_list
# from reports.views import report_post
# from post.views import post_list, create_post, post_detail, comment_detail, comment_create,reply_create, post_with_comments

urlpatterns = [
    #회원가입 로그인 및 로그아웃
    path("admin/", admin.site.urls),
    path('api/user/signup', user_signup_view, name='user_signup'),
    path('api/user/signin', phone_number_login, name='phone_number_login'),
    path('api/user/auto-signin', auto_signin, name='auto_login'),
    path('api/user/signout', user_logout_view, name='user_signout'),
    path('api/user/withdrawal', user_delete_view, name='user_withdrawal'),
    path('api/user/info', user_info_view, name='user_info'),
    path('api/user/token-refresh', token_refresh, name='token_refresh'),
    #게시판
    path('api/posts/create', create_post, name='post_create'),
    path('api/posts/<int:post_id>', post_detail, name='post_detail'),
    path('api/posts', post_list, name='post_list'),
    path('api/posts/<int:post_id>/sharing', update_sharing, name='post_list'),
    path('api/posts/<int:post_id>/report', create_postreport, name='create_postreport'),
    path('api/posts/<int:post_id>/like',post_like, name='post_like'),
    path('api/posts/<int:post_id>/comments', comment_create, name='comment_create'),
    path('api/posts/<int:post_id>/comments/<int:comment_id>', comment_detail, name='comment_detail'),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/report', comment_report, name='comment_report'),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/replies',create_reply, name='create_reply'),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/replies/<int:reply_id>', reply_detail, name='reply-detail'),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/replies/<int:reply_id>/report',reply_report, name='reply_report'),
    
    #버리기
    path('api/waste/image-upload', image_upload, name='image_upload'),
    #path('api/waste/apply', waste_apply, name='waste_apply'),
    
    #나의버니
    #path('api/myburni', , ),
    path('api/myburni/posts', sharing_list, name='sharing_list'),
]

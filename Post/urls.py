from django.urls import path,include
from . import views

urlpatterns=[
    path('post/',views.post_list,name="post_list"),    
    path('post/<int:pk>/',views.post_detail,name="post_detail"),
    path('post/<int:pk>/comments/',views.comment_list,name="comment_list"),    
    # path('test04/<int:pk>/',views.delete_comment,name="test04")  
]   
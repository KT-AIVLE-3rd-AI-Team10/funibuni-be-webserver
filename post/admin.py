from django.contrib import admin
from post.models import Post, Comment, Reply

# Post 모델을 관리자 페이지에 등록
admin.site.register(Post)

# Comment 모델을 관리자 페이지에 등록
admin.site.register(Comment)

# Reply 모델을 관리자 페이지에 등록
admin.site.register(Reply)



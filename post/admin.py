from django.contrib import admin
from post.models import Post, PostReport, PostLike, Comment, CommentReport, Reply, ReplyReport

admin.site.register(Post)
admin.site.register(PostReport)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentReport)
admin.site.register(Reply)
admin.site.register(ReplyReport)
from django.contrib import admin
from accounts.models import User
from accounts.models import OutstandingToken, BlacklistedToken
admin.site.register(User)
admin.site.register(OutstandingToken)
admin.site.register(BlacklistedToken)
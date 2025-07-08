from django.contrib import admin
from userauth.models import User

# Register your models here.

class useradmin(admin.ModelAdmin):
    list_display = ['username','email']

admin.site.register(User,useradmin)
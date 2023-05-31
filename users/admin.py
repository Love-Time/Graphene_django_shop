from django.contrib import admin
from .models import CustomUser, Settings, Theme
from django.apps import apps

class AdminUser(admin.ModelAdmin):
    list_display = ('id','email', 'last_name', 'first_name', 'is_staff', 'is_active', 'is_block')
# Register your models here.
admin.site.register(CustomUser, AdminUser)
admin.site.register(Settings)
admin.site.register(Theme)


app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)


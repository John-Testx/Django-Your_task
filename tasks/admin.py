from django.contrib import admin
from tasks.models import UserTasks, CommonUser

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("fechaInicio",)

admin.site.register(CommonUser)
admin.site.register(UserTasks, TaskAdmin)
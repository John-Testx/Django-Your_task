from django.contrib import admin
from projects.models import Project, ProjectRegistratedMembers,ProjectMember,ProjectAdmin, Stage , ProjectTask, ProjectInvitation

# Register your models here.
class ProjectoAdmin(admin.ModelAdmin):
    readonly_fields = ("fechaInicio",)
    list_display = ("nombre", "admin", "fechaTermino","proyecto_cerrado",)

class MemberAdmin(admin.ModelAdmin):
  list_display = ("person", "project", "date_joined", "charge")

class StageAdmin(admin.ModelAdmin):
  list_display = ("nombre", "project", "color")

class TaskAdmin(admin.ModelAdmin):
  list_display = ("nombre", "project", "stage", "encargado","completado","descripcion")

admin.site.register(Project, ProjectoAdmin)
admin.site.register(ProjectRegistratedMembers, MemberAdmin)
admin.site.register(ProjectTask,TaskAdmin)
admin.site.register(Stage,StageAdmin)
admin.site.register(ProjectInvitation)
admin.site.register(ProjectMember)
admin.site.register(ProjectAdmin)
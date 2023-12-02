from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.username

class CommonUser(BaseUser):
    esCommonUser = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Common User"
        verbose_name_plural = "Common Users"
    
class UserTasks(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaTermino = models.DateTimeField(null=True, blank=True)
    completado = models.BooleanField(default= False)
    user = models.ForeignKey(CommonUser, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Common User Task"
        verbose_name_plural = "Common User Tasks"
    
    def __str__(self):
        return self.nombre + ' by: ' + self.user.username
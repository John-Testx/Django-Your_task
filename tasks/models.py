from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserTasks(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaTermino = models.DateTimeField(null=True, blank=True)
    completado = models.BooleanField(default= False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre + ' by: ' + self.user.username
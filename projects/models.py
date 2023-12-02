from collections.abc import Iterable
import django
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from tasks.models import BaseUser
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ProjectAdmin(BaseUser):
    esProjectAdmin = models.BooleanField(default=True)
    class Meta:
        
        verbose_name = "Project Admin"
        verbose_name_plural = "Project Admins"

class ProjectMember(BaseUser):
    esProjectMember = models.BooleanField(default=True)
    class Meta:
        
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"
    
    
class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaTermino = models.DateTimeField(null=True, blank=True)
    proyecto_cerrado = models.BooleanField(default=False)
    admin= models.ForeignKey(ProjectAdmin, on_delete=models.CASCADE, related_name='ProjectAdmin')
    members = models.ManyToManyField(ProjectMember, through="ProjectRegistratedMembers")
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.nombre 

class Stage(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    color= models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Stage"
        verbose_name_plural = "Stages"
    
    def __str__(self):
        return self.nombre 

class ProjectRegistratedMembers(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(ProjectMember, on_delete=models.CASCADE, related_name='ProjectMember')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='Project')
    date_joined = models.DateTimeField(auto_now_add=True)
    charge = models.CharField(max_length=64, null=True)
    
    class Meta:
        verbose_name = "Project Registrated Member"
        verbose_name_plural = "Project Registrated Members"
    
    def __str__(self):
        return self.person.username 

class ProjectTask(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre= models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fechaInicio = models.DateTimeField()
    fechaTermino = models.DateTimeField(null=True, blank=True)
    etiquetas= models.CharField(max_length=100, null=True, blank=True)
    importancia= models.CharField(max_length=100, null=True, blank=True)
    encargado = models.ForeignKey(ProjectRegistratedMembers, on_delete=models.CASCADE, null=True, blank=True)
    completado = models.BooleanField(default=False)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    stage= models.ForeignKey(Stage, on_delete=models.CASCADE) 

    class Meta:
        verbose_name = "Project Task"
        verbose_name_plural = "Project Tasks"
    
    def __str__(self):
        return self.nombre 

class ProjectInvitation(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(ProjectAdmin, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(ProjectMember, on_delete=models.CASCADE, related_name='received_invitations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, editable=False)
    
    class Meta:
        verbose_name = "Project Invitation"
        verbose_name_plural = "Project Invitations"
    
    def __str__(self):
        return f"Invitation from {self.sender.username} to {self.recipient.username} for project {self.project.nombre}"
    
    def save(self, *args, **kwargs):
        
        self.sent_date = django.utils.timezone.now()
        
        formato = f"""{self.recipient} has sido invitado por {self.sender} a
                    \nunirte al proyecto {self.project.nombre}.
                    \nFecha de envio: {self.sent_date} """
        
        #these 3 variables are used to store the info of the email address and the message.
        subject = 'nueva reserva'
        body = formato
        to = [f'{self.recipient.email}']
        
        #La Clase EmailMessage funciona similar a la función send_email y toma como parametros el sujeto y el mensaje del correo,
        # la dirección de correo desde donde se esta enviando y por ultimo una lista con los que recibiran el correo. 
        msg = EmailMessage(subject, body, settings.EMAIL_HOST_USER, to)
        msg.send()
        
        return super(ProjectInvitation, self).save(*args, **kwargs)
    
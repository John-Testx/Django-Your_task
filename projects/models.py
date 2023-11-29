from collections.abc import Iterable
import django
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
    
class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaTermino = models.DateTimeField(null=True, blank=True)
    proyecto_cerrado = models.BooleanField(default=False)
    admin= models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    members = models.ManyToManyField(User, through="ProjectMembers")
    
    def __str__(self):
        return self.nombre 

class Stage(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    color= models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre 

class ProjectMembers(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='Project')
    date_joined = models.DateTimeField(auto_now_add=True)
    charge = models.CharField(max_length=64, null=True)
    
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
    encargado = models.ForeignKey(ProjectMembers, on_delete=models.CASCADE, null=True, blank=True)
    completado = models.BooleanField(default=False)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    stage= models.ForeignKey(Stage, on_delete=models.CASCADE) 

    def __str__(self):
        return self.nombre 

class ProjectInvitation(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, editable=False)
    
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
        
        return super().save(args, **kwargs) 
    
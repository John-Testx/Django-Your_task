from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from tasks.models import UserTasks
from tasks.forms import TaskCreateForm
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect 
from django.urls import reverse
from django.db import IntegrityError
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.


#Primera vista que da la bienvenida al sitio
def home(request):
    return render(request, 'home.html')


# Vista para registrarse
#Esta vista es para registrarse, aquí no use directamente el formulario por defecto que tiene django para crear usuarios si no 
#que hice mis propios input y luego de que el usuario haya ingresado de manera correcta ambas contraseñas y su nombre,
#se crea el usuario dentro de la base de datos, a partir de los datos que el usuario ingreso.
#Luego para que el usuario ya ingrese sesión inmediatamente se hace uso del metodo de django login y se le redirige al menu.
def signup(request):    
    if request.method == 'GET':
        print( 'Sending form registration')
        return render(request, 'signup.html',{
        'form': UserCreationForm 
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #register user
            try:
                user= User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'],email=request.POST['mail1'])
                user.save()
                login(request,user)
                return redirect('menu')
            except IntegrityError:
                return render(request, 'login.html',{
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request,'signup.html',{
            'form': UserCreationForm,
            'error':'Password do not match'})


# Vista para cerrar sesión
#Aquí se hace uso de un metodo de django el cual a partir de un request deslogea o elimina la sesión actual del usuario.
def loguserout(request):
    logout(request)
    return redirect('home')


# Vista para iniciar sesión
#Vista para ingresar con un usuario ya creado aquí se hace uso de un formulario por defecto de django "AuthenticationForm"
#y luego se verifica si el nombre de usuario y contraseña son correctos, esto también se hace a traves de un metodo de django 
#llamado authenticate, luego que esto sea exitoso se dirige al usuario al menu de tareas y proyectos.
def loguserin(request):
    if request.method == 'GET':
        return render(request,'login.html',{
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(request, username=request.POST['username'], 
        password=request.POST['password'])
        if user is None:
            return render(request,'login.html',{
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else:
            login(request,user)
            return redirect('menu')


# Vista de tareas de usuario
#from here, requires login 
#Task es la vista que muestra todas las tareas del usuario y la cual permite también crear tareas.
@login_required        
def task(request):
    if request.method == 'GET':
        tasks = UserTasks.objects.filter(user=request.user, fechaTermino__isnull=True).order_by('nombre')
        form = TaskCreateForm()
        return render(request, 'usertask.html',
        {'tasks': tasks, 'form': form})
    if request.method == 'POST':
        try:
            form = TaskCreateForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('usertask')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskCreateForm(),
            'error':'Please provide valid data'
        })
    
    return render(request, 'usertask.html',
        {'tasks': tasks, 'form': TaskCreateForm})     


# Vista de menú de usuario      
#Esta es la vista que le muestra al usuario para elegir entre las tareas y los proyectos.
@login_required
def menu(request):
    return render(request, 'menu.html')


# Marcar tarea como completada  
#Esta no es una vista como tal solo se hace un request para poder marcar como completada la tarea que se haya seleccionado
@login_required            
def complete_task(request, task_id):
    task = get_object_or_404(UserTasks, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.fechaTermino = timezone.now()
        task.completado= True;
        task.save()
        return redirect('usertask')

# Eliminar tarea
#Esta no es una vista como tal solo se hace un request para poder eliminar la tarea que se haya seleccionado
@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(UserTasks, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('usertask')


@login_required 
# Vista de perfil de usuario
def user_profile(request):    
    if request.method == 'POST':
        return render(request, 'profile.html')
    
    return render(request, 'profile.html')
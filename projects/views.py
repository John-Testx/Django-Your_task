from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from projects.models import Project, ProjectMembers, ProjectTask , Stage, ProjectInvitation
from projects.forms import FormCreateProject, FormTaskProject, FormCreateStage, FormUpdateTask , Form_invitations
from django.utils import timezone

# Create your views here.

# my_project es la vista donde se muestran los proyectos que tiene el usuario actualmente
# y donde también se le permite crear proyectos

# Decorador para requerir que el usuario esté autenticado para acceder a la vista
@login_required
def my_project(request):
    # Recopila todos los proyectos y miembros asociados al usuario
    project = Project.objects.filter().order_by('nombre').all()
    member = ProjectMembers.objects.filter(person=request.user)
    
    # Crea una instancia del formulario para crear un proyecto
    f = FormCreateProject()

    if request.method == 'GET':
        # Si la solicitud es GET, renderiza la página con el formulario y los proyectos del usuario
        return render(request, 'project.html', {'form': f, 'project': project, 'member': member})

    if request.method == 'POST':
        try:
            # Si la solicitud es POST, procesa el formulario para crear un nuevo proyecto
            form = FormCreateProject(request.POST)
            if form.is_valid():
                new_project = form.save(commit=False)
                new_project.admin = request.user
                new_project.save()

                # Creación de etapas predeterminadas para el nuevo proyecto
                stage_1 = Stage.objects.create(nombre="To Do", project=new_project, color="#ffaf00")
                stage_2 = Stage.objects.create(nombre="In Progress", project=new_project, color="#dc143c")
                stage_3 = Stage.objects.create(nombre="Done", project=new_project, color="#7fff00")

                return redirect('project')

        except ValueError:
            # Si ocurre una excepción, vuelve a renderizar la página con un mensaje de error
            project = Project.objects.filter(admin=request.user).order_by('nombre').all()
            return render(request, 'create_project.html', {
                'form': FormCreateProject,
                'error': 'Por favor, proporciona datos válidos',
                'project': project
            })

    return render(request, 'project.html', {'project': project, 'form': FormCreateProject, 'member': member})


#project_view ahora mismo solo muestra la tabla kanban y muestra las tareas que estan creadas para que el usuario las vea
#cada proyecto al crearse genera unas etapas por defecto las cuales son: To Do, In Progress, Done

@login_required
def project_view(request,project_id):
    stage= Stage.objects.filter(project=project_id)
    task= ProjectTask.objects.filter(project=project_id).order_by('nombre').all()
    member= ProjectMembers.objects.filter(project=project_id)
    project= get_object_or_404(Project, id=project_id)
    
    f= FormTaskProject()
    f_s= FormCreateStage()
    f.onlyProjectStages(project_id)
    
    if request.method == 'POST':     
        
        try:
            project= get_object_or_404(Project, id=project_id)
            form = FormTaskProject(request.POST)
            form_stage= FormCreateStage(request.POST)
            
            if form.is_valid():
                stage= get_object_or_404(Stage, id=request.POST['stage'])
                new_task = form.save(commit=False)
                new_task.project = project
                new_task.stage = stage
                new_task.save()
            
            if form_stage.is_valid():
                new_stage = form_stage.save(commit=False)
                new_stage.project = project
                new_stage.save()
            
            return redirect('project_view',project_id)
        
        except ValueError: 
            stage= Stage.objects.filter(project=project_id)
            project= get_object_or_404(Project, id=project_id)
            task= ProjectTask.objects.filter(project=project_id).order_by('nombre').all()
            member= ProjectMembers.objects.filter(project=project_id)
            
            f= FormTaskProject()
            f.onlyProjectStages(project_id)
            
            return render(request, 'project_view.html', { 'task':task, 'stage':stage, 'form':f,
            'error':'Please provide valid data', 'project': project, 'member':member})
        
        
    return render (request, 'project_view.html',
                   {'task':task, 'stage':stage, 'form':f ,'member':member,'project':project,'form_s':f_s})

@login_required    
def delete_project_task(request, project_id, task_id):
    task = get_object_or_404(ProjectTask, pk=task_id, project=project_id)
    if request.method == 'POST':
        task.delete()
        print('task deleted successfully')
        return redirect('project_view',project_id)

@login_required
def get_task_details(request, task_id):
    try:
        task = ProjectTask.objects.filter(pk=task_id).values(
            'id', 'nombre', 'descripcion', 'project__id', 'stage__nombre', 'completado'
        ).first()
        
        if task:
            return JsonResponse(task)
        else:
            return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def update_task(request, project_id, task_id):
    try:
        if request.method == 'POST':
            task = get_object_or_404(ProjectTask, pk=task_id, project=project_id)
            form = FormUpdateTask(request.POST, instance=task)

            if form.is_valid():
                form.save()
                return redirect('project_view',project_id) 
            else:
                return JsonResponse({'error': form.errors}, status=400)

    except ProjectTask.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
    except Exception as e:
        # Log the exception details
        print(f"Exception in update_task view: {str(e)}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    
@login_required            
def complete_project_task(request, project_id, task_id):
    try:
        if request.method == 'POST':
            task = get_object_or_404(ProjectTask, pk=task_id, project= project_id)
            task.fechaTermino = timezone.now()
            task.completado= True;
            print(task)
            task.save()
            return redirect('project_view', project_id)
        
    except ProjectTask.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
def delete_stage(request, project_id, stage_id):
    try:
        if request.method == 'POST':
            stage= get_object_or_404(Stage, pk=stage_id, project=project_id)
            stage.delete()
            return redirect('project_view', project_id)
    except ValueError:
        return redirect('project_view', project_id)

@login_required
def delete_project(request, project_id):
    try:
        if request.method == 'POST':
            project= get_object_or_404(Project, pk=project_id)
            project.delete()
            return redirect('project')
    except ValueError:
        return redirect('project_view', project_id)
    
@login_required
def exit_project(request, project_id):
    try:
        if request.method == 'POST':
            member= get_object_or_404(ProjectMembers, project=project_id, person=request.user)
            member.delete()
            return redirect('project')
            
    except ValueError:
        return redirect('project_view', project_id)

@login_required
def delete_member(request,project_id,member_id):
    try:
        if request.method == 'POST':
            member= get_object_or_404(ProjectMembers, project=project_id, person=member_id)
            member.delete()
            return redirect('project_view', project_id)
    except ValueError:
        return redirect('project_view', project_id)


################################

#Invitaciones
    
@login_required
def show_invitations(request):
    invite= ProjectInvitation.objects.filter(recipient=request.user)
    return render(request, 'invitations.html',{'invite':invite})


@login_required
def make_invitation(request, project_id):
    invitacion= Form_invitations()
    invitacion.onlyYourProject(project_id)

    return render(request, 'make_invitation.html', {'form':invitacion})

@login_required
def accept_invitations(request, invitation_id):
    try:
        invite= ProjectInvitation.objects.filter(recipient=request.user)
        if request.method == 'POST':
            invite= get_object_or_404(ProjectInvitation, id=invitation_id, recipient=request.user)
            invite.accepted= True
            
            x= ProjectMembers.objects.create(person=request.user, project=invite.project, charge='member')
            x.save()
            invite.delete()
            return redirect('invitations')
    except Exception as e:
        print('error: ',e)
        return redirect('invitations')
    
@login_required
def decline_invitation(request, invitation_id):
    try:
        invite= ProjectInvitation.objects.filter(recipient=request.user)
        if request.method == 'POST':
            invite= get_object_or_404(ProjectInvitation, id=invitation_id, recipient=request.user)
            invite.delete()
            return redirect('invitations')
    except Exception as e:
        print('error: ',e)
        return redirect('invitations')

    

# def output_to_file(text):
#     with open('debug_log.txt', 'a') as f:
#         f.write(text + "\n")
# message= "Tu invitacion al proyecto :s".format(x.project.nombre)
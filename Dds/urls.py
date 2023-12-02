"""Dds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from projects import views as vP


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #home and login paths
    path('',views.home, name='home'),
    path('signup/',views.signup, name="signup"),
    path('login/',views.loguserin, name="login"),
    path('logout/',views.loguserout, name="logout"),
    path('menu/',views.menu, name="menu"),
    
    #Project Invitations
    path('invitations/',vP.show_invitations, name="invitations"),
    path('invitations/make/<int:project_id>', vP.make_invitation, name="make_invitation"),
    path('invitations/send/<int:project_id>/<int:user_id>', vP.send_invitation, name="send_invitation"),
    path('invitations/accept/<int:invitation_id>',vP.accept_invitations, name="accept_invitation"),
    path('invitations/accept/<int:invitation_id>',vP.decline_invitation, name="decline_invitation"),
    
    #Task (user) paths
    path('profile/',views.user_profile, name="user_profile"),
    path('tasks/',views.task, name="usertask"),
    path('tasks/<int:task_id>/complete',views.complete_task, name="complete_task"),
    path('tasks/<int:task_id>/delete',views.delete_task, name="delete_task"),
    
    #Project (Project) paths
    path('project/',vP.my_project, name="project"),
    path('project/view/<int:project_id>',vP.project_view, name="project_view"),
    path('project/view/<int:project_id>/<int:task_id>/',vP.delete_project_task, name="project_delete_task"),
    
    #Task paths
    path('get_task_details/<int:task_id>/', vP.get_task_details, name='get_task_details'),
    path('get_task_dates/<int:project_id>/', vP.get_task_by_date, name='get_task_dates'),
    path('update_task_details/<int:project_id>/<int:task_id>',vP.update_task, name='update_task_details'),
    path('complete_project_task/<int:project_id>/<int:task_id>',vP.complete_project_task, name='complete_project_task'),
    
    #Delete paths
    path('project/view/stage/<int:project_id>/<int:stage_id>/',vP.delete_stage, name='delete_stage'),
    path('project/view/delete_this/<int:project_id>',vP.delete_project, name="delete_project"),
    path('project/view/exit_this/<int:project_id>',vP.exit_project, name="exit_project"),
    path('project/view/delete_member/<int:project_id>/<int:member_id>',vP.delete_member, name="delete_member"),
]

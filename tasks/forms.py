from django import forms
from tasks.models import UserTasks
from django.contrib.auth.models import User

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model= UserTasks
        fields= ['nombre','descripcion']
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control ','placeholder':'write a name',
                                            'style': 'width: 100%; '}),
            'descripcion':forms.Textarea(attrs={'class':'form-control ','placeholder':'write some description','rows':'2'}),
        }

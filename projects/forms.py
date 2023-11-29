from django import forms
from projects.models import Project, ProjectTask, Stage, ProjectMembers, ProjectInvitation

class FormCreateProject(forms.ModelForm):
    class Meta:
        model=Project
        fields=['nombre','descripcion','fechaTermino']
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control ','placeholder':'write a name',}),
            'descripcion':forms.Textarea(attrs={'class':'form-control ','placeholder':'write some description','rows':'2'}),
            'fechaTermino':forms.DateInput(attrs={'class':'form-control','type':'date'})
        }

class FormCreateStage(forms.ModelForm):
    class Meta:
        model=Stage
        fields=['nombre','color']
        
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre...'}), label="Nombre de la etapa:")
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'color'}), label="Color de la etapa:")
        
        
class FormUpdateTask(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ['nombre', 'descripcion',]
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control ','placeholder':'write a name',}),
            'descripcion':forms.Textarea(attrs={'class':'form-control ','placeholder':'write some description','rows':'2'}),}

        
class FormTaskProject(forms.ModelForm):
    class Meta:
        model=ProjectTask
        fields=['nombre','descripcion','fechaInicio','fechaTermino','stage','encargado']
    
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre...'}), label="Nombre")
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribir descripción....', 'rows': '2'}), label="Descripción")
    fechaInicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label="Fecha de Inicio")
    fechaTermino = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label="Fecha de Termino")
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label="Etapa de proyecto")
    encargado = forms.ModelChoiceField(queryset=ProjectMembers.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label="Definir encargado")
    

    def onlyProjectStages(self, user=None, **kwargs):
        self.fields['stage'].queryset = Stage.objects.filter(project=user)
        self.fields['encargado'].queryset = ProjectMembers.objects.filter(project=user)
        
class Form_invitations(forms.ModelForm):
    class Meta:
        model = ProjectInvitation
        fields = '__all__'
        
    def onlyYourProject(self, id=None, **kwargs):
        self.fields['project'].queryset = Project.objects.filter(id=id)
        
        
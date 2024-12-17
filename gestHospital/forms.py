from django import forms
from .models import Lesion

class registro_paciente(forms.Form):
    MUJER = 'M'
    HOMBRE = 'H'
    OTRO = 'NS/NR'
    SEXO_CHOICES = (
        (MUJER, 'Female'),
        (HOMBRE, 'Male'),
        (OTRO, 'Other')
    )
    NUM_SS = 'SSN'
    OTRO = 'NIF/NIE'
    DOC_CHOICES = (
        (NUM_SS, 'Social Security Number'),
        (OTRO, 'NIF/NIE')
    )
    
    LESIONES_CHOICES = sorted([
        ('hombro', 'Shoulder'),
        ('codo', 'Elbow'),
        ('muñeca', 'Wrist'),
        ('mano', 'Hand'),
        ('cadera', 'Hip'),
        ('rodilla', 'Knee'),
        ('tobillo', 'Ankle'),
        ('pie', 'Foot'),
        ('columna_cervical', 'Cervical Spine'),
        ('columna_dorsal', 'Thoracic Spine'),
        ('columna_lumbar', 'Lumbar Spine'),
        ('cuadriceps', 'Quadriceps'),
        ('isquiotibiales', 'Hamstrings'),
        ('gemelos', 'Calves'),
        ('pectoral', 'Pectoral'),
        ('dorsal', 'Back'),
        ('trapecio', 'Trapezius'),
        ('abdomen', 'Abdomen')
    ], key=lambda x: x[1])

    Nombre = forms.CharField(label='First Name', max_length=25)
    Apellidos = forms.CharField(label='Last Name', max_length=40)
    Sexo = forms.ChoiceField(choices=SEXO_CHOICES)
    NumId = forms.CharField(label='Identifier', help_text='Social Security Number or any other mutual recognition number by the state. If unavailable, register NIF or NIE.')
    Documentacion = forms.ChoiceField(choices=DOC_CHOICES)
    Lesion = forms.ModelMultipleChoiceField(
        queryset=Lesion.objects.all(),
        widget=forms.SelectMultiple,
        label="Injuries"
    )


class registro_ingreso(forms.Form):
    Paciente = forms.CharField(label='Patient ID', max_length=30)
    Edad = forms.IntegerField(min_value=0, max_value=150, label='Patient Age')
    Fecha_ingreso = forms.DateField(required=True)
    Fecha_alta = forms.DateField(required=False, localize=True)
    Descripcion = forms.CharField(label='Description', max_length=2000, required=False)
    Medico = forms.CharField(label='Doctor', max_length=20, required=False)

class BuscarPaciente(forms.Form):
    texto = forms.CharField(label='Search Text', max_length=50)

class ModificarIngreso(forms.Form):
    Paciente = forms.CharField(label='Patient ID', max_length=30, required=False)
    Edad = forms.IntegerField(min_value=0, max_value=150, label='Patient Age', required=False)
    Fecha_ingreso = forms.DateField(required=False)
    Fecha_alta = forms.DateField(required=False)
    Descripcion = forms.CharField(label='Description', max_length=2000, required=False)
    Medico = forms.CharField(label='Doctor', max_length=20, required=False)

class registro_medico(forms.Form):
    TRAUMATOLOGIA = 'trauma'
    CIRUGIA = 'surgery'
    CARDIOLOGIA = 'cardiology'
    NEUROLOGIA = 'neurology'
    UROLOGIA = 'urology'
    OFTALMOLOGIA = 'ophthalmology'

    ESPECIALIDA_CHOICES = (
        (TRAUMATOLOGIA, 'Traumatology'),
        (CIRUGIA, 'Surgery'),
        (CARDIOLOGIA, 'Cardiology'),
        (NEUROLOGIA, 'Neurology'),
        (UROLOGIA, 'Urology'),
        (OFTALMOLOGIA, 'Ophthalmology')
    )

    NumColegiado = forms.CharField(label='License Number', max_length=20, required=True)
    Especialidad = forms.ChoiceField(choices=ESPECIALIDA_CHOICES, required=True)
    Password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput(), required=True)

class LogInUsuarios(forms.Form):
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'password'}))

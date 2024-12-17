from django.db import models

class Lesion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.nombre

class Paciente(models.Model):
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

    Documentacion = models.CharField(max_length=25, choices=DOC_CHOICES, default=NUM_SS)
    NumId = models.CharField(max_length=20, primary_key=True, help_text='Social Security Number or any other mutuality recognized by the state. If unavailable, register NIF or NIE.')
    Nombre = models.CharField(max_length=25)
    Apellidos = models.CharField(max_length=40)
    Sexo = models.CharField(choices=SEXO_CHOICES, default=OTRO, max_length=10)
    Lesiones = models.ManyToManyField(Lesion, blank=True)  # Relacion de muchos a muchos

    def __str__(self):
        return f'{self.Nombre} {self.Apellidos}'

class Ingreso(models.Model):
    Paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    Edad = models.IntegerField()
    Fecha_ingreso = models.DateTimeField()
    Fecha_alta = models.DateTimeField(blank=True, null=True)
    Descripcion = models.CharField(max_length=2000, blank=True, null=True)

class Medico(models.Model):
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

    NumColegiado = models.CharField(max_length=20, primary_key=True, help_text="License Number")
    Especialidad = models.CharField(choices=ESPECIALIDA_CHOICES, max_length=15)
    Ingresos = models.ManyToManyField(Ingreso)

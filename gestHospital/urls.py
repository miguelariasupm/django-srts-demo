from django.urls import path
from . import views

urlpatterns = [
    path('', views.bienvenida, name='gestHospital-bienvenida'),
    path('historia/', views.getHistoria, name='gestHospital-historia'),
    path('noticias/', views.getNoticias, name='gestHospital-noticias'),
    path('pacientes/formularios/registrar-paciente', views.FormRegPaciente, name='gestHospital-r-f-paciente'),
    path('pacientes/formularios/seleccionar-paciente/', views.formSelecPaciente, name='gestHospital-s-f-paciente'),
    path('ingresos/formularios/registrar-ingreso', views.FormRegIngreso, name='gestHospital-r-f-ingreso'),
    path('pacientes/mostrar/paciente', views.mostrarPacientes, name='gestHospital-m-paciente' ),
    path('pacientes/borrar/<str:NumId>/', views.borrarPacientes, name='gestHospital-e-paciente'),
    path('pacientes/mostrar/<str:NumId>/', views.mostrarPaciente, name='gestHospital-v-paciente'),
    path('ingresos/mostrar/ingreso', views.mostrarIngresos , name='gestHospital-m-ingreso' ),
    path('ingresos/borrar/<str:id>/', views.borrarIngresos, name='gestHospital-e-ingreso'),
    path('ingresos/formularios/editar/<str:id>/', views.editarIngreso, name='gestHospital-m-f-ingreso'),
    path('medicos/formularios/registrar-medico', views.FormRegMedico, name='gestHospital-r-f-medico'),
    path('login/', views.logIn, name='gestHospital-login'),
    path('logout/', views.logOut, name='gestHospital-logout'),
    path('seleccionar-ordenar/', views.seleccionar_ordenar, name='gestHospital-ordenar')
]
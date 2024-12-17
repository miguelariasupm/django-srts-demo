from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from gestHospital.forms import *
from gestHospital.hospitales import *
from .models import Paciente, Ingreso, Medico
from .hospitales import ETIQUETA_ASCENDENTE, ETIQUETA_DESCENDENTE, ETIQUETA_APELLIDO, ETIQUETA_FECHA

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout

from django.db.models import Avg

# Create your views here.

NEXT_FIELD_LABEL = 'next'

ETIQUETA_ORDENAR = 'orden'
ETIQUETA_CATEGORIA = 'caracteristica'

BIENVENIDA = 'gestHospital/base.html'
HISTORIA   = 'gestHospital/historia.html'
NOTICIAS = 'gestHospital/noticias.html'
LOGIN_USUARIOS = 'gestHospital/login.html'

REG_PACIENTE = 'gestHospital/registro_paciente.html'
REG_INGRESO = 'gestHospital/registro_ingreso.html'
LISTA_PACIENTES = 'gestHospital/lista_pacientes.html'
LISTA_INGRESOS = 'gestHospital/lista_ingresos.html'
MOSTRAR_PACIENTE = 'gestHospital/mostrarpaciente.html'
MOD_INGRESO='gestHospital/modificarIngreso.html'
REG_MEDICO = 'gestHospital/registro_medico.html'

RESULTADO = 'gestHospital/res.html'

def bienvenida( request ):
    return render (request, BIENVENIDA)

def getHistoria( request ):
    return render( request, HISTORIA )

def getNoticias ( request ):
    return render (request, NOTICIAS)

def logIn( request ):
    if ( request.method == 'POST'):
        form = LogInUsuarios(request.POST)
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        else:
            error='Por favor, habilite las cookies para continuar'
            return render(request, LOGIN_USUARIOS, {'formulario':form, 'errorMsg':error })
        form = LogInUsuarios(request.POST)
        if ( form.is_valid()):
            nombreUsuario = form.cleaned_data['username']
            contrasenya = form.cleaned_data['password']
            usuario = authenticate(request, username=nombreUsuario, password=contrasenya)
            if ( usuario ):
                if ( request.user.is_authenticated ):
                    logout(request)
                login(request, usuario)
                nextPage=request.GET.get(NEXT_FIELD_LABEL)
                if ( nextPage is None ):
                    nextPage = reverse('gestHospital-bienvenida')
                return redirect (nextPage)
            else:
                error='Nombre de usuario o contraseña incorrectos'
                return render(request, LOGIN_USUARIOS, {'formulario':form, 'errorMsg':error })
        else:
            error="Los datos de algún campo del formulario son incorrectos"
            return render(request, LOGIN_USUARIOS, {'formulario':form, 'errorMsg':error })
    else:
        form = LogInUsuarios()
        if ( request.GET.get('error403') is None):
            error=None
        else:
            error='Operación no permitida. Use una cuenta con permisos suficientes'
        request.session.set_test_cookie()
        return render(request, LOGIN_USUARIOS, {'formulario':form, 'errorMsg': error })

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_ingreso'], raise_exception=True)
def seleccionar_ordenar( request ):
    if ( request.method=='GET'):
        btn = request.GET['btn']
        if btn == 'apellidos':
            categoria = request.session[ETIQUETA_CATEGORIA]=ETIQUETA_APELLIDO
        else:
            categoria = request.session[ETIQUETA_CATEGORIA]=ETIQUETA_FECHA
        orden = request.session.get(ETIQUETA_ORDENAR)
        if ( not orden) :
            orden = request.session[ETIQUETA_ORDENAR]=ETIQUETA_DESCENDENTE
            pass
        else:
            if ( orden == ETIQUETA_ASCENDENTE):
                orden = request.session[ETIQUETA_ORDENAR]=ETIQUETA_DESCENDENTE
                pass
            else:
                orden = request.session[ETIQUETA_ORDENAR]=ETIQUETA_ASCENDENTE
                pass
        lista = GestorIngreso.buscarIngresos(Usuario(request.user.username), orden, categoria)
        edad_media = Medico.objects.get(NumColegiado=request.user.username).Ingresos.values('Paciente__Sexo').annotate(Avg('Edad'))
        return render(request, LISTA_INGRESOS, {'lista': lista, 'edad_media':edad_media})
    else:
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Búsqueda de granjas"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
    
@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=BIENVENIDA)
def logOut( request ):
    logout( request )
    return redirect ('gestHospital-bienvenida')

# views.py
from django.shortcuts import render
from .forms import registro_paciente
from .models import Paciente, Lesion

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required(['gestHospital.add_paciente'], raise_exception=True)
def FormRegPaciente(request):
    if request.method == 'GET':
        form = registro_paciente()
        return render(request, REG_PACIENTE, {'formulario': form})

    if request.method == 'POST':
        form = registro_paciente(request.POST)
        if form.is_valid():
            print(form.cleaned_data['Lesion'])
            # Recibe los datos del formulario
            num_id = form.cleaned_data['NumId']
            nombre = form.cleaned_data['Nombre']
            apellidos = form.cleaned_data['Apellidos']
            sexo = form.cleaned_data['Sexo']
            documentacion = form.cleaned_data['Documentacion']
            lesiones = form.cleaned_data['Lesion']  # Lista de lesiones seleccionadas

            # Crea un nuevo paciente y guarda
            paciente = Paciente(
                Nombre=nombre,  # Cambiar 'nombre' por 'Nombre'
                Apellidos=apellidos,  # Cambiar 'apellidos' por 'Apellidos'
                Sexo=sexo,  # Cambiar 'sexo' por 'Sexo'
                NumId=num_id,  # Cambiar 'num_id' por 'NumId'
                Documentacion=documentacion  # Cambiar 'documentacion' por 'Documentacion'
            )
            paciente.save()

            # Asocia las lesiones al paciente usando la relación ManyToMany
            paciente.Lesiones.set(lesiones)  # Asocia las lesiones seleccionadas
            paciente.save()

            texto = f"Patient with ID: {num_id} correctly added"
            return render(request, RESULTADO, {'texto': texto, "texto_op": "New patient register", 'paciente': True})
        else:
            # Si hay errores en el formulario
            error = "Error al registrar el paciente"
            return render(request, REG_PACIENTE, {'formulario': form, 'errorMsg': error, 'paciente': True})





@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_paciente'], raise_exception=True)
def formSelecPaciente(request):
    if (request.method != 'POST'):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Búsqueda de pacientes"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
        pass

    form = BuscarPaciente(request.POST)
    if (form.is_valid()):
        texto = form.cleaned_data['texto']
        lista = GestorPaciente.buscar(texto)
        return render(request, LISTA_PACIENTES, {'lista': lista})
        pass
    else:
        error = "No se ha podido completar la búsqueda"
        op = "Búsqueda de pacientes"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.delete_paciente'], raise_exception=True)
def borrarPacientes(request, NumId):
    res = GestorPaciente.borrarPaciente(NumId)
    if ( res is None):
        error = "No existe el paciente con identificador " + NumId
        op = "Eliminar granja"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op, 'tablapaciente': True })
        pass
    else:
        texto = "Patient with ID " + NumId + " was deleted"
        op = "Delete patient"
        return render(request, RESULTADO, {'texto': texto, "texto_op" : op, 'tablapaciente': True })
        pass
    pass

    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_paciente'], raise_exception=True)
def mostrarPacientes(request):
    if (request.method == 'GET'):
        lista = GestorPaciente.buscarPaciente()
        return render(request, LISTA_PACIENTES, {'lista': lista})
        pass

    error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
    op = "Búsqueda de pacientes"
    return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_paciente'], raise_exception=True)
def mostrarPaciente(request, NumId):
    res = GestorPaciente.buscarPaciente(NumId)
    if ( res is None):
        error = "No existe el paciente con identificador " + NumId
        op = "Buscar paciente"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op, 'tablapaciente': True })
        pass
    else:
        return render(request, MOSTRAR_PACIENTE, {'paciente': res, 'tablapaciente': True})
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.add_ingreso'], raise_exception=True)
def FormRegIngreso(request):
    if ((request.method != 'GET') and (request.method != 'POST')):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Registro de un nuevo ingreso"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)

    if (request.method == 'GET'):
        form = registro_ingreso(request.POST)
        return render (request, REG_INGRESO, {'formulario': form})

    if (request.method == 'POST'):
        form = registro_ingreso(request.POST)
        if (form.is_valid()):
            Paciente = form.cleaned_data['Paciente']
            Edad = form.cleaned_data['Edad']
            Fecha_ingreso = form.cleaned_data['Fecha_ingreso']
            Fecha_alta = form.cleaned_data['Fecha_alta']
            Descripcion = form.cleaned_data['Descripcion']
            Medico = form.cleaned_data['Medico']
            res = GestorIngreso.registrarIngreso(Paciente, Edad, Fecha_ingreso, Fecha_alta, Descripcion,Medico)
            if (res['code'] == 0):
                texto = "Ingreso del paciente con identificador "+ Paciente +" añadido correctamente."
                op = "Registro de un nuevo ingreso"
                return render(request, RESULTADO, {'texto': texto, "texto_op" : op, 'ingreso': True}) 
            else:
                error = "Error en el registro del ingreso"
                return render(request, REG_INGRESO, {'formulario': form, 'errorMsg': error, 'ingreso': True})
        pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_ingreso'], raise_exception=True)
def mostrarIngresos(request):
    if (request.method == 'GET'):
        lista = GestorIngreso.buscarIngresos(Usuario(request.user.username),request.session.get(ETIQUETA_ORDENAR),request.session.get(ETIQUETA_CATEGORIA))
        edad_media = Medico.objects.get(NumColegiado=request.user.username).Ingresos.values('Paciente__Sexo').annotate(Avg('Edad'))
        return render(request, LISTA_INGRESOS, {'lista': lista, 'edad_media':edad_media})

    error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
    op = "Búsqueda de ingresos"
    return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_ingreso'], raise_exception=True)
def mostrarIngreso(request, id):
    res = GestorIngreso.buscarIngreso(id)
    if ( res is None):
        error = "No existe el ingreso con identificador " + id
        op = "Buscar ingreso"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.change_ingreso'], raise_exception=True)
def editarIngreso( request, id):
    if ((request.method != 'GET') and (request.method != 'POST')):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Modificación de ingreso"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
        pass

    ingreso = Ingreso.objects.get(id = id)

    if (request.method == 'GET'):
        form =ModificarIngreso(request.POST)
        return render (request, MOD_INGRESO, {'formulario': form, 'ingreso': ingreso})
        pass
    
    op = "Modificar un ingreso"
    if (request.method == 'POST'):
        form = ModificarIngreso(request.POST)
        if ( form.is_valid()):
            NumId = form.cleaned_data['Paciente']
            descripcion = form.cleaned_data['Descripcion']
            fecha_alta = form.cleaned_data['Fecha_alta']
            fecha_ingreso = form.cleaned_data['Fecha_ingreso']
            edad = form.cleaned_data['Edad']
            medico = form.cleaned_data['Medico']

            user = Usuario(request.user.username)
            
            if ingreso.Fecha_alta:
                if descripcion:
                    res = GestorIngreso.modificarIngreso(id, Descripcion=descripcion)
                    if res == 0:
                        texto = "Se ha modificado la descripción del ingreso" + id +".\n El resto de campos no se han podido modificar puesto que ya se había ingresado la fecha de alta"
                        return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
                    else:
                        error = "Error general"
                        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op})
                elif medico and user.es_administrador:
                    res = GestorIngreso.modificarIngreso(id, Medico=medico)
                    if res == 0:
                        texto = "Se ha asignado el ingreso " + id +" al médico " + medico
                        return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
                    else:
                        error = "Error general"
                        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op})
                elif fecha_alta and user.es_staff:
                    res = GestorIngreso.modificarIngreso(id, Fecha_alta=fecha_alta)
                    if res == 0:
                        texto = "Se ha modificado la fecha de alta a " + fecha_alta
                        return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
                    else:
                        error = "Error general"
                        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op})
                else:
                    error = "Error, no se puede modificar un campo distinto a 'Descripción' o asignar a un médico si ya se ha registrado la fecha de alta"
                    return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op})

            elif NumId or edad or fecha_alta or fecha_ingreso or descripcion :
                res = 0
                if NumId and user.es_administrador:
                    paciente = Paciente.objects.get(NumId=NumId)
                    res = GestorIngreso.modificarIngreso(id, Paciente=paciente)
                if edad  and res == 0 and user.es_administrador:
                    res = GestorIngreso.modificarIngreso(id, Edad=edad)
                if descripcion and res==0:
                    res = GestorIngreso.modificarIngreso(id, Descripcion=descripcion)
                if fecha_alta and res==0:
                    res = GestorIngreso.modificarIngreso(id, Fecha_alta=fecha_alta)
                if fecha_ingreso and res==0 and user.es_administrador:
                    res = GestorIngreso.modificarIngreso(id, Fecha_ingreso=fecha_ingreso)
                
            if res == 0:
                texto = "El ingreso "+ id +" ha sido modificado"
                return render(request, RESULTADO, {'texto': texto, "texto_op" : op})
                pass

            elif res  == 1:
                error = "El ingreso "+ id +" no existe"
                return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op})
                pass

            elif res == 2:
                error = "Error general"
                return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op})
                pass
            else:
                texto = "No se ha modificado ningún campo del ingreso " + id
                return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
                pass
            pass
        
        else:
            form = ModificarIngreso(request.POST)
            error="Error en el formulario"
            return render(request, MOD_INGRESO, {'formulario': form, 'errorMsg': error})
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.delete_ingreso'], raise_exception=True)
def borrarIngresos(request, id):
    res = GestorIngreso.borrarIngreso(id)
    if ( res is None):
        error = "No existe el ingreso con identificador " + id
        op = "Eliminar ingreso"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    else:
        texto = "Ingreso con identificador " + id + " ha sido borrada"
        op = "Eliminar ingreso"
        return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.add_medico'], raise_exception=True)
def FormRegMedico(request):

    if ((request.method != 'GET') and (request.method != 'POST')):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Registro de un nuevo medico"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)

    if (request.method == 'GET'):
        form = registro_medico(request.GET)
        return render (request, REG_MEDICO, {'formulario': form})

    if (request.method == 'POST'):
        form = registro_medico(request.POST)
        if (form.is_valid()):
            numColegiado = form.cleaned_data['NumColegiado']
            especialidad = form.cleaned_data['Especialidad']
            password = form.cleaned_data['Password']
            res = GestorMedico.registrarMedico(NumColegiado=numColegiado,Especialidad=especialidad,Password=password)
            if (res['code'] == 0):
                texto = "Médico con identificador "+ numColegiado +" añadido correctamente"
                op = "Registro de un nuevo médico"
                return render(request, RESULTADO, {'texto': texto, "texto_op" : op, 'medico': True }) 
            else:
                error = "Error"
                if (res['code'] == 1):
                    error = 'Ya existe el médico con identificador: '+ numColegiado
                    pass
                return render(request, REG_MEDICO, {'formulario': form, 'errorMsg': error, 'medico': True })
        pass

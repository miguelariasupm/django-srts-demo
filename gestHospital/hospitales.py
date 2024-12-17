from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User, Group


from .models import Paciente, Ingreso, Medico

GRUPO_STAFF = 'staff'
GRUPO_ADMINISTRADORES = 'administradores'

ETIQUETA_ASCENDENTE = 'ASC'
ETIQUETA_DESCENDENTE = 'DSC'
ETIQUETA_APELLIDO = 'APE'
ETIQUETA_FECHA = 'FEC'

class Usuario:
    nombre_usuario : str = ''
    es_administrador : bool = False
    es_staff : bool = False

    def __init__(self, nombre_usuario : str) -> None:
        try:
            usuario = User.objects.get(username=nombre_usuario)
            pass
        except ObjectDoesNotExist:
            return

        self.nombre_usuario = usuario.username
        self.es_administrador = usuario.groups.all().filter(name__iexact=GRUPO_ADMINISTRADORES).count() == 1 or usuario.is_superuser
        self.es_staff = usuario.groups.all().filter(name__iexact=GRUPO_STAFF).count() == 1
        pass

    def esAdministrador(self) :
        return self.es_administrador


class GestorPaciente:
    def registrarPaciente(Nombre, Apellidos, Sexo , Documentacion, NumId):
        try:
            Paciente.objects.get(NumId=NumId)
            res = {'code':1}
        except ObjectDoesNotExist:
            paciente = Paciente(Nombre= Nombre, Apellidos= Apellidos, Sexo=Sexo, Documentacion=Documentacion, NumId=NumId )
            try:
                paciente.save()
                res = {'code' : 0}
            except IntegrityError:
                res = {'code' : 2}
        return res
    
    def buscarPaciente( NumId=None ):
        if ( NumId is None ):
            pacientes = list( Paciente.objects.all())
            return pacientes
            pass
        else:
            try:
                paciente = Paciente.objects.get(NumId = NumId)
                return paciente
                pass
            except ObjectDoesNotExist:
                return None
                pass
            pass
        pass

    def buscar( texto ):
        if ( texto is None):
            return None
            pass
        lista = list(Paciente.objects.filter(NumId=texto) | Paciente.objects.filter( Nombre=texto)| Paciente.objects.filter( Apellidos=texto))
        return lista        
        pass

    def borrarPaciente(NumId):
        if ( NumId is None ):
            return None
        try:
            paciente = Paciente.objects.get( NumId = NumId)
            paciente.delete()
            return paciente
            pass
        except ObjectDoesNotExist:
            return None
            pass
        pass
    pass

class GestorIngreso:

    def registrarIngreso(NumId, Edad, Fecha_ingreso, Fecha_alta, Descripcion = None, Medico = None):
        paciente = Paciente.objects.get(NumId = NumId)
        ingreso = Ingreso(Paciente=paciente, Edad=Edad, Fecha_ingreso=Fecha_ingreso, Fecha_alta=Fecha_alta, Descripcion=Descripcion)
        try:
            ingreso.save() 
            try:
                GestorMedico.anadirIngreso(Medico,ingreso.id)
                return {'code' : 0}
            except:
                return {'code' : 1}
        except IntegrityError:
            return {'code' : 1}
        
    def buscarIngreso( id=None ):
        if ( id is None ):
            ingresos = list( Ingreso.objects.all())
            return ingresos
            pass
        else:
            try:
                ingreso = Ingreso.objects.get(id = id)
                return ingreso
                pass
            except ObjectDoesNotExist:
                return None
                pass
            pass
        pass

    def buscarIngresos(usuario : Usuario, orden : str, categoria : str):
        if (usuario.es_administrador):
            ingresos = Ingreso.objects.all()
        else:
            ingresos = Medico.objects.get(NumColegiado=usuario.nombre_usuario).Ingresos.all()
        if (categoria == ETIQUETA_FECHA):
            if (orden == ETIQUETA_DESCENDENTE):
                ingresos = ingresos.order_by('-Fecha_ingreso')
            else:
                ingresos = ingresos.order_by('Fecha_ingreso')
        else:
            if (orden == ETIQUETA_DESCENDENTE):
                ingresos = ingresos.order_by('-Paciente__Apellidos')
            else:
                ingresos = ingresos.order_by('Paciente__Apellidos')

        return list(ingresos)

    def borrarIngreso(id):
        if ( id is None ):
            return None
        try:
            ingreso = Ingreso.objects.get( id = id)
            ingreso.delete()
            return ingreso
            pass
        except ObjectDoesNotExist:
            return None
            pass
        pass
    pass
    
    def modificarIngreso( id, NumId = None, Edad = None, Fecha_ingreso = None, Fecha_alta = None , Descripcion = None, Medico = None):
        try:
            ingreso=Ingreso.objects.get( id = id )
            if Edad:
                ingreso.Edad = Edad
            if NumId:
                paciente =Paciente.objects.get(NumId = NumId)
                ingreso.Paciente = paciente
            if Fecha_ingreso:
                ingreso.Fecha_ingreso=Fecha_ingreso
            if Fecha_alta:
                ingreso.Fecha_alta=Fecha_alta
            if Descripcion:
                ingreso.Descripcion= Descripcion
            if Medico:
                GestorMedico.anadirIngreso(Medico,id)

            ingreso.save();
            return 0
        except ObjectDoesNotExist:
            return 1
        except IntegrityError:
            return 2
        
class GestorMedico:
    def registrarMedico(NumColegiado,Especialidad,Password):
        try:
            Medico.objects.get(NumColegiado=NumColegiado)
            return {'code':1}
        except ObjectDoesNotExist:
            try:
                User.objects.get(username=NumColegiado)
                return {'code':1}
            except ObjectDoesNotExist:
                pass

        try:
            grupo_adm = Group.objects.get(name=GRUPO_STAFF)
            pass
        except ObjectDoesNotExist:
            return {'code': 3}

        medico = Medico(NumColegiado=NumColegiado, Especialidad=Especialidad)
        usuario = User.objects.create_user(username=NumColegiado,password=Password)
        try:
            usuario.groups.add(grupo_adm)
            usuario.save()
            try:
                medico.save()
            except:
                return {'code':4}
            return {'code' : 0}
        except IntegrityError:
            return {'code' : 2}
        
    def anadirIngreso(numColegiado, idIngreso):
        try:
            medico = Medico.objects.get(NumColegiado=numColegiado)
            try:
                medico.Ingresos.get(id=idIngreso)
                return 3
            except ObjectDoesNotExist:
                ingreso = Ingreso.objects.get(id=idIngreso)
                medico.Ingresos.add(ingreso)
                medico.save()
        except ObjectDoesNotExist:
            return 2
        return 0
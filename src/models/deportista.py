import enum
from datetime import datetime
from sqlalchemy import UUID, Column, Integer, Enum, String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from .model import Model
from .db import Base


class TipoIdentificacionEnum(str, enum.Enum):
    tarjeta_identidad = "tarjeta_identidad"
    cedula_ciudadania = "cedula_ciudadania"
    cedula_extranjeria = "cedula_extranjeria"
    pasaporte = "pasaporte"
    registro_civil = "registro_civil"


class GeneroEnum(str, enum.Enum):
    masculino = "masculino"
    femenino = "femenino"
    otro = "otro"


class Deportista(Model, Base):
    __tablename__ = "deportista"
    nombre = Column(String(50))
    apellido = Column(String(50))
    tipo_identificacion = Column(Enum(TipoIdentificacionEnum))
    numero_identificacion = Column(BigInteger)
    email = Column(String(50), unique=True)
    genero = Column(Enum(GeneroEnum))
    edad = Column(Integer)
    peso = Column(Float)
    altura = Column(Float)
    pais_nacimiento = Column(String(50))
    ciudad_nacimiento = Column(String(50))
    pais_residencia = Column(String(50))
    ciudad_residencia = Column(String(50))
    antiguedad_residencia = Column(Integer)
    contrasena = Column(String(50))
    id_plan_subscripcion = Column(UUID(as_uuid=True), ForeignKey('plan_subscripcion.id'))
    
    plan_subscripcion: Mapped['PlanSubscripcion'] = relationship("PlanSubscripcion", backref="deportistas")

    def __init__(self, **info_deportista):
        Model.__init__(self)
        self.__dict__.update(info_deportista)

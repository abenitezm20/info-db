from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from .model import Model
from sqlalchemy.orm import relationship
from .db import Base


class DetalleSubscripcion(Model, Base):
    __tablename__ = "detalle_subscripcion"
    beneficios = Column(String(10000))
    id_plan_subscripcion = Column(UUID, ForeignKey('plan_subscripcion.id'))
    plan_subscripcion = relationship('PlanSubscripcion')

    def __init__(self, **info_detalle_subscripcion):
        Model.__init__(self)
        self.__dict__.update(info_detalle_subscripcion)
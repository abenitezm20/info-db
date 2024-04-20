from .db import Base

from src.models.tipo_plan_alimenticio import TipoPlanAlimenticio
from src.models.menu import Menu
from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class PlanAlimenticio(Model, Base):
    __tablename__ = "plan_alimenticio"
    id_tipo_plan_alimenticio = Column(UUID(as_uuid=True), ForeignKey('tipo_plan_alimenticio.id'), primary_key=True)
    id_menu = Column(UUID(as_uuid=True), ForeignKey('menu.id'), primary_key=True)

    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250), nullable=False)
    id_plan = Column(UUID(as_uuid=True))
    
    
    tipo_plan_alimenticio: Mapped['TipoPlanAlimenticio'] = relationship("TipoPlanAlimenticio")
    menu: Mapped['Menu'] = relationship("Menu")


    def __init__(self, id_tipo_plan_alimenticio, id_menu, nombre, descripcion, id_plan):
        Model.__init__(self)
        self.id_tipo_plan_alimenticio = id_tipo_plan_alimenticio
        self.id_menu = id_menu
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_plan = id_plan

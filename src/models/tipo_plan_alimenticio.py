from .db import Base
from sqlalchemy import Column, String
from src.models.model import Model


class TipoPlanAlimenticio(Model, Base):
    __tablename__ = "tipo_plan_alimenticio"
    nombre = Column(String(50), unique=True, nullable=False)

    def __init__(self, nombre):
        Model.__init__(self)
        self.nombre = nombre

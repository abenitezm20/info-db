from .db import Base
from sqlalchemy import Column, String, Integer
from src.models.model import Model


class Menu(Model, Base):
    __tablename__ = "menu"

    nombre = Column(String(50), unique=True, nullable=False)
    calorias = Column(Integer)
    porcion = Column(Integer)
    medida = Column(String(5))
    descripcion = Column(String(250))

    def __init__(self, nombre, calorias, porcion, medida, descripcion):
        Model.__init__(self)
        self.nombre = nombre
        self.calorias = calorias
        self.porcion = porcion
        self.medida = medida
        self.descripcion = descripcion

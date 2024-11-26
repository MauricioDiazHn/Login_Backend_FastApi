from sqlalchemy import Column, Integer, String, Date, VARBINARY, NCHAR
from database import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    CodUsuario = Column(String(50), nullable=False, unique=True, index=True)
    Nombre = Column(String(50), nullable=True)
    FechaSys = Column(Date, nullable=True)
    Funcion = Column(String(50), nullable=True)
    Cargo = Column(String(50), nullable=True)
    Sucursal = Column(String(50), nullable=True)
    CuentaCaja = Column(String(25), nullable=True)
    Email = Column(String(40), nullable=True)
    Activo = Column(String(1), nullable=True)
    Pass = Column(VARBINARY, nullable=True)
    Almacen = Column(String(30), nullable=True)
    CentroCosto = Column(NCHAR(20), nullable=True)
    IdEmpleado = Column(NCHAR(15), nullable=True)
    NombrePuesto = Column(String(200), nullable=True)

from pydantic import BaseModel
from typing import Optional
from datetime import date

class TokenData(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CreateUserRequest(BaseModel):
    CodUsuario: str
    Nombre: str
    FechaSys: Optional[date] = None
    Funcion: Optional[str] = None
    Cargo: Optional[str] = None
    Sucursal: Optional[str] = None
    CuentaCaja: Optional[str] = None
    Email: str
    Activo: Optional[str] = "Y"  
    Password: str
    Almacen: Optional[str] = None
    CentroCosto: Optional[str] = None
    IdEmpleado: Optional[str] = None
    NombrePuesto: Optional[str] = None

class CreateUserResponse(BaseModel):
    ID: int
    CodUsuario: str
    Nombre: str
    Email: str


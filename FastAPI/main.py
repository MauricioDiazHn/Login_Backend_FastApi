from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Usuario
from sqlalchemy import func

from auth import create_access_token, verify_password, get_password_hash, decode_access_token
from schemas import TokenData, TokenResponse, CreateUserRequest, CreateUserResponse
from fastapi.security import OAuth2PasswordBearer
from datetime import date

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["sub"]

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.post("/usuarios/", response_model=CreateUserResponse)
def create_user(user_data: CreateUserRequest, db: Session = Depends(get_db)):
    
    existing_user = db.query(Usuario).filter(Usuario.CodUsuario == user_data.CodUsuario).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso.",
        )
    existing_email = db.query(Usuario).filter(Usuario.Email == user_data.Email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está en uso.",
        )
    
    hashed_password = get_password_hash(user_data.Password)
    binary_password = hashed_password.encode('utf-8')
    
    
    new_user = Usuario(
        CodUsuario=user_data.CodUsuario,
        Nombre=user_data.Nombre,
        FechaSys=user_data.FechaSys or date.today() or func.getdate(),
        Funcion=user_data.Funcion,
        Cargo=user_data.Cargo,
        Sucursal=user_data.Sucursal,
        CuentaCaja=user_data.CuentaCaja,
        Email=user_data.Email,
        Activo=user_data.Activo,
        Pass=binary_password, 
        Almacen=user_data.Almacen,
        CentroCosto=user_data.CentroCosto,
        IdEmpleado=user_data.IdEmpleado,
        NombrePuesto=user_data.NombrePuesto,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "ID": new_user.ID,
        "CodUsuario": new_user.CodUsuario,
        "Nombre": new_user.Nombre,
        "Email": new_user.Email,
    }

@app.post("/login", response_model=TokenResponse)
def login(data: TokenData, db: Session = Depends(get_db)):
    
    user = db.query(Usuario).filter(Usuario.CodUsuario == data.username).first()
    
    if not user or not verify_password(data.password, user.Pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.CodUsuario})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/usuarios/")
def read_usuarios(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        usuarios = db.query(Usuario).all() 
        return [
            {
            "ID": u.ID,
            "CodUsuario": u.CodUsuario,
            "Nombre": u.Nombre,
            "Email": u.Email,
            "Activo": u.Activo
        }
        for u in usuarios
        ]
    except Exception as e:
        return {"error": str(e)} 

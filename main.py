from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI(title="API de Usuarios")

# Modelo de datos para validación (Pydantic)
class UsuarioCrear(BaseModel):
    nombre: str
    email: EmailStr

class Usuario(UsuarioCrear):
    id: int

# Base de datos en memoria
usuarios: list[Usuario] = [
    Usuario(id=1, nombre="Ana", email="ana@example.com"),
    Usuario(id=2, nombre="Carlos", email="carlos@example.com"),
]

# 1. Obtener todos los usuarios
@app.get("/api/usuarios", response_model=list[Usuario])
def obtener_usuarios():
    return usuarios

# 2. Obtener un usuario por ID
@app.get("/api/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    for u in usuarios:
        if u.id == usuario_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# 3. Crear un nuevo usuario
@app.post("/api/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCrear):
    nuevo_id = len(usuarios) + 1 if usuarios else 1
    nuevo_usuario = Usuario(id=nuevo_id, **usuario.model_dump())
    usuarios.append(nuevo_usuario)
    return nuevo_usuario

# 4. Eliminar un usuario
@app.delete("/api/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    global usuarios
    usuarios_iniciales = len(usuarios)
    usuarios = [u for u in usuarios if u.id != usuario_id]
    
    if len(usuarios) == usuarios_iniciales:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return {"mensaje": f"Usuario con ID {usuario_id} eliminado"}
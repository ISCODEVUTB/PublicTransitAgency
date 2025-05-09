from fastapi import APIRouter, Request, Form, status, HTTPException
from fastapi.responses import RedirectResponse
from jose import jwt
from backend.app.core.config import settings
from backend.app.core.auth import encode_token
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from backend.app.core.deps import *
import os

# Simulated user store with hardcoded credentials (replace with real user DB/service)
fake_users_db = {
    "admin": {"username": "admin", "password": "adminpass", "scope": "administrador", "email": "admin@domain.com", "tel": "123456789", "ID": 1, "Nombre": "Administrador", "Apellido": "Admin", "Contrasena": "adminpass", "IDRolUsuario": 1, "IDTurno": 1},
    "pasajero": {"username": "john", "password": "pasajeropass", "scope": "pasajero", "email": "john@domain.com", "tel": "987654321", "ID": 2, "Nombre": "John", "Apellido": "Doe", "Contrasena": "pasajeropass", "IDRolUsuario": 2, "IDTurno": 1},
    "supervisor": {"username": "jane", "password": "supervisorpass", "scope": "supervisor", "email": "jane@domain.com", "tel": "111222333", "ID": 3, "Nombre": "Jane", "Apellido": "Smith", "Contrasena": "supervisorpass", "IDRolUsuario": 3, "IDTurno": 2},
    "Tecnico": {"username": "Joshph", "password": "tecnicopass", "scope": "mantenimiento", "email": "joshph@domain.com", "tel": "444555666", "ID": 4, "Nombre": "Joshph", "Apellido": "Technico", "Contrasena": "tecnicopass", "IDRolUsuario": 4, "IDTurno": 3},
}

app = APIRouter(prefix="/login", tags=["login"])
templates = Jinja2Templates(directory="src/frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    print("[LOGIN GET] Rendering login form")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    payload = {
        "sub": user["username"],
        "scope": user["scope"]
    }

    token = encode_token(payload)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/", response_class=HTMLResponse)
async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    print(f"[LOGIN POST] Attempting login for user: {username}")

    user = fake_users_db.get(username)

    if not user or user["password"] != password:
        print("[LOGIN POST] Invalid credentials")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    scope = user["scope"]
    print(f"[LOGIN POST] Authenticated. Scope: {scope}")

    payload = {
        "sub": username,
        "scope": scope
    }

    token = encode_token(payload)
    print(f"[LOGIN POST] Token generated: {token}")

    response = RedirectResponse(url=request.url_for("get_scope_page", scope=scope), status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)

    return response

@app.get("/user/{scope}", name="get_scope_page", response_class=HTMLResponse)
async def get_scope_page(request: Request, scope: str):
    try:
        token_cookie = request.cookies.get("access_token", "").replace("Bearer ", "")
        user_data = {"username": "Unknown", "scope": scope}

        if token_cookie:
            try:
                payload = jwt.decode(token_cookie, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_data["username"] = payload.get("sub", "Unknown")
                user_data["scope"] = payload.get("scope", "Unknown")
            except JWTError as e:
                print(f"[SCOPE GET] Token decode error: {e}")

        user = fake_users_db.get(user_data["username"], {})

        # Verificar si el ID está presente en los datos del usuario
        user_id = user.get("ID", "No ID found")

        # Pasamos los datos completos del usuario a la plantilla
        return templates.TemplateResponse(f"{scope}.html", {
            "request": request,
            "user": user,
            "id": user_id,
            "total_vehiculos": total_unidades(),
            "total_passanger": total_pasajeros(),
            "total_operative": total_operario(),
            "total_supervisors": total_supervisor(),
            "type_card": get_type_card(user_id),
            "buses_mantenimiento": total_unidades(),
            "registros_mantenimiento": total_mantenimiento(),
            "proximo_mantenimiento": proximos_mantenimientos(),
            "ultimo_uso_tarjeta": last_card_used(user_id),
            "nombre":"None",
            "turno":"None",
            "zona":"None"
        })

    except Exception as e:
        print(f"[SCOPE GET] ERROR: {e}")
        return HTMLResponse(f"<h1>Template error: {e}</h1>", status_code=500)

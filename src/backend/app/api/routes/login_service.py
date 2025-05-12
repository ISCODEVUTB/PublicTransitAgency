from starlette.responses import HTMLResponse, RedirectResponse
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, Request, HTTPException, status, APIRouter, Form
from fastapi.templating import Jinja2Templates
from backend.app.core.auth import encode_token, settings
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.user import UserCreate, UserOut
from backend.app.core.deps import total_unidades, total_pasajeros, total_operario, total_supervisor, total_mantenimiento, proximos_mantenimientos, last_card_used,get_type_card

# Crear el controlador para acceder a la base de datos
controller = UniversalController()

app = APIRouter(prefix="/login", tags=["login"])
templates = Jinja2Templates(directory="src/frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    print("[LOGIN GET] Rendering login form")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = controller.get_by_column(UserCreate, "ID", form_data.username)

    if not user or user.Contrasena != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    scope = map_role_to_scope(user.IDRolUsuario)

    payload = {
        "sub": user.Nombre,
        "scope": scope
    }

    token = encode_token(payload)
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/", response_class=HTMLResponse)
async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    print(f"[LOGIN POST] Attempting login for ID: {username}")
    user = controller.get_by_column(UserOut, "ID", username)
    print(f"[LOGIN POST] Resultado de user: {user}")
    if not user or user.Contrasena != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    scope = map_role_to_scope(user.IDRolUsuario)

    payload = {
        "sub": username,
        "scope": scope
    }

    token = encode_token(payload)
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

        user = controller.get_by_column(UserOut, "ID", user_data["username"])
        user_id = user.ID if user else "No ID found"

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


def map_role_to_scope(role_id: int) -> str:
    role_scope_map = {
        1: "pasajero",
        2: "operador",
        3: "supervisor",
        4: "administrador",
        5: "mantenimiento"
    }
    return role_scope_map.get(role_id, "guest")

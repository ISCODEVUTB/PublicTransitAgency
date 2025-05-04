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
import os

# Simulate user store with hardcoded credentials (replace with real user DB/service)
fake_users_db = {
    "admin": {"username": "admin", "password": "adminpass", "scope": "administrador"},
    "john": {"username": "john", "password": "johnpass", "scope": "pasajero"},
    "jane": {"username": "jane", "password": "janepass", "scope": "supervisor"},
    "pedro": {"username": "pedro", "password": "pedropass", "scope": "tecnico"},
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

    # Generamos el payload con un único scope
    payload = {
        "sub": user["username"],
        "scope": user["scope"]  # 'scope' es solo una cadena
    }

    token = encode_token(payload)  # Esto debería ser la función que genera el JWT

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
        token_cookie = request.cookies.get("access_token", "")
        if token_cookie.startswith("Bearer "):
            token_cookie = token_cookie.replace("Bearer ", "")

        user_data = {"username": "Unknown", "scope": scope}

        if token_cookie:
            try:
                payload = jwt.decode(token_cookie, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_data["username"] = payload.get("sub", "Unknown")
                user_data["scope"] = payload.get("scope", "Unknown")
            except JWTError as e:
                print(f"[SCOPE GET] Token decode error: {e}")
                raise HTTPException(status_code=401, detail="Invalid token")

        template_path = f"{scope}.html"
        full_path = os.path.join("src/frontend/templates", template_path)

        print(f"[SCOPE GET] Requested scope: {scope}")
        print(f"[SCOPE GET] Full template path: {full_path}")
        print(f"[SCOPE GET] Exists: {os.path.exists(full_path)}")

        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail=f"Template '{template_path}' not found.")

        return templates.TemplateResponse(template_path, {
            "request": request,
            "user": user_data
        })

    except Exception as e:
        print(f"[SCOPE GET] ERROR: {e}")
        return HTMLResponse(f"<h1>Template error: {e}</h1>", status_code=500)
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.sessions import SessionMiddleware

from App.dao.UsuarioDAO import UsuarioDAO
from App.models.UsuarioModel import UsuarioRegistro
from App.models.RespuestaModel import Salida

# Routers importados
from routers.usuarios_router import router as usuarios_router
from routers.barberias_router import router as barberias_router
from routers.barberos_router import router as barberos_router
from routers.servicios_router import router as servicios_router
from routers.citas_router import router as citas_router
from routers.cliente_router import router as cliente_router

# Conexión a MongoDB
from BD.conexion import Conexion

app = FastAPI(
    title="StyleCut REST API 💈",
    description="Sistema de gestión para barberías",
    version="1.0.0",
    docs_url=None
)

app.add_middleware(SessionMiddleware, secret_key="supersecreto")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluimos los routers
app.include_router(usuarios_router)
app.include_router(barberias_router)
app.include_router(barberos_router)
app.include_router(servicios_router)
app.include_router(citas_router)
app.include_router(cliente_router)

# Ruta raíz → login visual
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    error = request.query_params.get("error")
    msg = None
    if error == "unauthorized":
        msg = "⚠️ Acceso solo para administradores"
    elif error == "login_failed":
        msg = "⚠️ Correo o contraseña incorrectos"
    return templates.TemplateResponse("login.html", {"request": request, "error": msg})

# Ruta POST del login visual
@app.post("/entrar")
async def entrar(request: Request, correo: str = Form(...), password: str = Form(...)):
    dao = UsuarioDAO(app.db)
    resultado = dao.autenticarUsuario(correo, password)

    if resultado.estatus == "OK":
        request.session["idUsuario"] = resultado.usuario.idUsuario
        request.session["tipo"] = resultado.usuario.tipo
        request.session["nombre"] = resultado.usuario.nombre

        if resultado.usuario.tipo == "Admin":
            return RedirectResponse(url="/docs", status_code=302)
        else:
            return RedirectResponse(url="/cliente/citas", status_code=302)
    else:
        return RedirectResponse(url="/?error=login_failed", status_code=302)

# Ruta GET para mostrar formulario de registro
@app.get("/registrar", response_class=HTMLResponse)
async def registrar_get(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})

# Ruta POST para procesar formulario de registro
@app.post("/registrar")
async def registrar_post(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    password: str = Form(...)
):
    dao = UsuarioDAO(app.db)

    nuevo_usuario = UsuarioRegistro(
        nombre=nombre,
        apellido=apellido,
        correo=correo,
        telefono=telefono,
        password=password
    )

    resultado: Salida = dao.registrarUsuario(nuevo_usuario)

    if resultado.estatus == "OK":
        return RedirectResponse(url="/", status_code=302)
    else:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": resultado.mensaje
        })

# Ruta protegida para ver Swagger solo si es Admin
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(request: Request):
    tipo = request.session.get("tipo")
    if tipo == "Admin":
        return get_swagger_ui_html(openapi_url=app.openapi_url, title="StyleCut API Docs")
    return RedirectResponse(url="/?error=unauthorized", status_code=302)

# Ruta para cerrar sesión (logout)
@app.get("/salir")
async def salir(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)

# Conexión a la base de datos al iniciar
@app.on_event("startup")
def startup():
    print("✅ Conectando a MongoDB...")
    conexion = Conexion()
    app.conexion = conexion
    app.db = conexion.getDB()

# Cierre de conexión al apagar
@app.on_event("shutdown")
def shutdown():
    print("🔚 Cerrando conexión con MongoDB...")
    app.conexion.cerrar()

# Ejecutar como script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("App.main:app", host="127.0.0.1", port=8000, reload=True)

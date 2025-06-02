from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from BD.conexion import Conexion

# Routers
from routers.citas_router import router as citas_router
from routers.usuarios_router import router as usuarios_router
from routers.servicios_router import router as servicios_router
from routers.barberias_router import router as barberias_router
from routers.barberos_router import router as barberos_router

app = FastAPI(
    title="StyleCut API REST",
    description="Sistema de gestión para barberías",
    version="1.0.0"
)

# Templates y archivos estáticos
templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")


# Routers por entidad
app.include_router(usuarios_router)
app.include_router(barberias_router)
app.include_router(barberos_router)
app.include_router(servicios_router)
app.include_router(citas_router)

# Página de inicio con login visual
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Validación de acceso (simulada o conectada a Mongo)
@app.post("/entrar")
async def entrar(correo: str = Form(...), password: str = Form(...)):
    if correo == "juan@gmail.com" and password == "1234":
        return RedirectResponse(url="/docs", status_code=302)
    return {"mensaje": "Credenciales incorrectas"}

# Conexión a Mongo
@app.on_event("startup")
def startup():
    print("✅ Conectando a MongoDB")
    conexion = Conexion()
    app.conexion = conexion
    app.db = conexion.getDB()

@app.on_event("shutdown")
def shutdown():
    print("🛑 Cerrando conexión con MongoDB")
    app.conexion.cerrar()

if __name__ == '__main__':
    uvicorn.run("App.main:app", host="127.0.0.1", port=8000, reload=True)

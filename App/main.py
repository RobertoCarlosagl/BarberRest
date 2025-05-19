from fastapi import FastAPI
import uvicorn
from BD.conexion import Conexion

# Importa tus routers
from routers.citas_router import router as citas_router
from routers.usuarios_router import router as usuarios_router
from routers.servicios_router import router as servicios_router
from routers.barberias_router import router as barberias_router

app = FastAPI(
    title="StyleCut API REST",
    description="Sistema de gestión para barberías",
    version="1.0.0"
)

# Incluir routers
app.include_router(citas_router)
app.include_router(usuarios_router)
app.include_router(servicios_router)
app.include_router(barberias_router)

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a StyleCut REST API 💈"}

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


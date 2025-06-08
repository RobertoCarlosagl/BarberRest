from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from App.dao.CitaDAO import CitaDAO
from datetime import date, time

router = APIRouter(
    prefix="/cliente",
    tags=["Cliente"]
)

templates = Jinja2Templates(directory="templates")

# GET - Formulario para agendar cita
@router.get("/citas/agendar", response_class=HTMLResponse)
async def cargar_formulario_agendar(request: Request):
    db = request.app.db

    barberias_activas = list(db.barberias.find({"estatus": "Activa"}, {"_id": 1, "nombre": 1}))
    barberia_ids_activas = [b["_id"] for b in barberias_activas]

    pipeline_barberos = [
        {"$match": {"estatus": "Activo", "idBarberia": {"$in": barberia_ids_activas}}},
        {"$lookup": {
            "from": "usuarios",
            "localField": "idUsuario",
            "foreignField": "_id",
            "as": "usuario"
        }},
        {"$unwind": "$usuario"},
        {"$match": {"usuario.tipo": "Barbero", "usuario.estatus": "Activo"}}
    ]
    barberos = list(db.barberos.aggregate(pipeline_barberos))

    servicios = list(db.servicios.find({"barberia_id": {"$in": barberia_ids_activas}}, {"_id": 1, "nombre": 1, "precio": 1, "barberia_id": 1}))

    return templates.TemplateResponse("cliente_agendar.html", {
        "request": request,
        "barberias": barberias_activas,
        "barberos_json": jsonable_encoder(barberos),
        "servicios_json": jsonable_encoder(servicios)
    })

# POST - Agendar cita
@router.post("/citas/agendar")
async def agendar_cita(
    request: Request,
    barberia_id: int = Form(...),
    barbero_id: int = Form(...),
    fecha: date = Form(...),
    hora: time = Form(...),
    servicios: list[str] = Form(...)
):
    db = request.app.db
    id_cliente = request.session.get("idUsuario")
    if not id_cliente:
        return RedirectResponse(url="/", status_code=302)

    cita_data = {
        "idCliente": id_cliente,
        "idBarbero": barbero_id,
        "fecha": fecha,
        "hora": hora,
        "servicios": servicios
    }

    dao = CitaDAO(db)
    resultado = dao.agendarCita(cita_data)

    if resultado.estatus == "OK":
        return RedirectResponse(url="/cliente/citas", status_code=302)
    else:
        return HTMLResponse(content="Error al agendar cita: " + resultado.mensaje, status_code=400)

# GET - Ver todas las citas del cliente
@router.get("/citas", response_class=HTMLResponse)
async def ver_mis_citas(request: Request):
    db = request.app.db
    id_cliente = request.session.get("idUsuario")
    if not id_cliente:
        return RedirectResponse(url="/", status_code=302)

    citas = list(db.citas.find({"idCliente": id_cliente}))
    return templates.TemplateResponse("cliente_dashboard.html", {"request": request, "citas": citas})

# POST - Cancelar cita
@router.post("/citas/{id}/cancelar")
async def cancelar_cita(id: int, request: Request):
    db = request.app.db
    id_cliente = request.session.get("idUsuario")
    if not id_cliente:
        return RedirectResponse(url="/", status_code=302)

    dao = CitaDAO(db)
    resultado = dao.cancelarCita(str(id), {"motivo": "Cancelación desde vista cliente"})
    return RedirectResponse(url="/cliente/citas", status_code=302)

# POST - Confirmar cita
@router.post("/citas/{id}/confirmar")
async def confirmar_cita(id: int, request: Request):
    db = request.app.db
    id_cliente = request.session.get("idUsuario")
    if not id_cliente:
        return RedirectResponse(url="/", status_code=302)

    dao = CitaDAO(db)
    resultado = dao.confirmarCita(str(id))
    return RedirectResponse(url="/cliente/citas", status_code=302)

# GET - Formulario para actualizar cita
@router.get("/citas/{id}/editar", response_class=HTMLResponse)
async def editar_cita(id: str, request: Request):
    db = request.app.db
    id_cliente = request.session.get("idUsuario")
    if not id_cliente:
        return RedirectResponse(url="/", status_code=302)

    cita = db.citas.find_one({"_id": id, "idCliente": id_cliente})
    if not cita:
        return HTMLResponse(content="Cita no encontrada o acceso denegado", status_code=404)

    barberias = list(db.barberias.find({"estatus": "Activa"}, {"_id": 1, "nombre": 1}))
    barberia_ids = [b["_id"] for b in barberias]
    barberos = list(db.barberos.aggregate([
        {"$match": {"estatus": "Activo", "idBarberia": {"$in": barberia_ids}}},
        {"$lookup": {
            "from": "usuarios",
            "localField": "idUsuario",
            "foreignField": "_id",
            "as": "usuario"
        }},
        {"$unwind": "$usuario"},
        {"$match": {"usuario.tipo": "Barbero", "usuario.estatus": "Activo"}}
    ]))
    servicios = list(db.servicios.find({"barberia_id": {"$in": barberia_ids}}, {"_id": 1, "nombre": 1, "precio": 1, "barberia_id": 1}))

    return templates.TemplateResponse("cliente_editar_cita.html", {
        "request": request,
        "cita": cita,
        "barberias": barberias,
        "barberos_json": jsonable_encoder(barberos),
        "servicios_json": jsonable_encoder(servicios)
    })

# POST - Actualizar cita
@router.post("/citas/{id}/editar")
async def actualizar_cita(
    id: str,
    request: Request,
    barberia_id: int = Form(...),
    barbero_id: int = Form(...),
    fecha: date = Form(...),
    hora: time = Form(...),
    servicios: list[str] = Form(...)
):
    db = request.app.db
    id_cliente = request.session.get("idUsuario")
    if not id_cliente:
        return RedirectResponse(url="/", status_code=302)

    dao = CitaDAO(db)
    datos_actualizados = {
        "idBarbero": barbero_id,
        "fecha": fecha,
        "hora": hora,
        "servicios": servicios
    }
    resultado = dao.actualizarCita(id, datos_actualizados)

    return RedirectResponse(url="/cliente/citas", status_code=302)

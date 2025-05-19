# BarberRest
Proyecto de barberia llamado "StyleCut" donde desarrollaremos servicios rest 

# StyleCut API REST 💈

Sistema de gestión de barberías desarrollado como parte del proyecto final de la materia **Arquitectura de Servicios (8° semestre)**.

Este repositorio contiene una API REST construida con FastAPI y MongoDB, organizada para pruebas directas con Swagger y Postman.

---

## ✅ ¿Qué contiene este repositorio?

📁 **App/** – Lógica principal de la aplicación  
📁 **BD/** – Conexión y colecciones MongoDB en formato JSON  
📁 **documentation/** – Tablas REST, evidencias y documentación Word  
📄 **README.md** – Este archivo  
📄 **.gitignore** – Evita subir `.venv`, cachés, configuraciones locales

---

## ⚙️ Requisitos previos

- Python 3.10 o superior
- MongoDB (ejecutando local en `localhost:27017`)
- FastAPI & Uvicorn (`pip install fastapi uvicorn pymongo`)

---

## 🚀 ¿Cómo ejecutar el proyecto?

### 1. Clona el repositorio

```bash
git clone https://github.com/TU_USUARIO/StyleCut.git
cd StyleCut

2. Crea un entorno virtual
python -m venv .venv


3. Activa el entorno virtual
.venv\Scripts\activate

4. Instala dependencias
pip install -r requirements.txt

Si no existe requirements.txt, puedes generarlo con:
pip freeze > requirements.txt

5. Ejecuta el servidor
uvicorn App.main:app --reload
🔗 Abre tu navegador y entra a:
http://127.0.0.1:8000/docs


Datos de prueba
En la carpeta BD/colecciones encontrarás archivos .json con datos simulados para cargar en MongoDB Compass.

Colecciones incluidas:
usuarios
barberos
barberias
citas
servicios
detalles

🧾 Autores
Roberto Carlos Mejía Aguilera – Gestión de Citas

Sergio de Jesús Valdés Peredo – Usuarios, Servicios, Barberías, Barberos

📄 Documentación adicional
Revisa la carpeta /documentation para ver:
Tablas REST completas de las 12 operaciones
Evidencias de pruebas
Documento entregable del proyecto (Word)


from fastapi import FastAPI, Depends, UploadFile, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import List, Dict, Any

from . import models, schemas
from .database import engine, get_db, SessionLocal
from .migrations import upgrade_schema
from .pdf_parser import extract_pdf_data
from .seed import seed_defaults
from .services.galileu_import import preview_registros, confirm_registros
from .services.legacy_adapter import list_alunos_legacy, get_aluno_legacy
from .routers import modalidades, turmas, pessoas, matriculas, mensalidades, metrics, auth, admin

upgrade_schema()

with SessionLocal() as db:
    seed_defaults(db)

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger("kannon_do_api")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "api.log"),
    maxBytes=10485760,
    backupCount=5,
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = FastAPI(title="Kannon Do API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(modalidades.router)
app.include_router(turmas.router)
app.include_router(pessoas.router)
app.include_router(matriculas.router)
app.include_router(mensalidades.router)
app.include_router(metrics.router)
app.include_router(admin.router)

logger.info("API iniciada e configurada.")


@app.get("/")
def read_root():
    return {"message": "API Financeira Kannon Do rodando."}


@app.post("/upload-pdf-preview/")
async def upload_pdf_preview(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logger.info(f"Recebido arquivo para preview: {file.filename}")
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        registros = extract_pdf_data(file_location)
        logger.info(f"Extraídos {len(registros)} registros do PDF.")
        return preview_registros(db, registros)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)


@app.post("/upload-pdf-confirm/")
async def upload_pdf_confirm(registros: List[Dict[str, Any]] = Body(...), db: Session = Depends(get_db)):
    try:
        processados = confirm_registros(db, registros)
        return {"status": f"{processados} registros processados/atualizados com sucesso no banco!"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/alunos/")
def read_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_alunos_legacy(db, skip=skip, limit=limit)


@app.get("/alunos/{aluno_id}", response_model=schemas.AlunoComHistorico)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando detalhes do aluno ID: {aluno_id}")
    aluno = get_aluno_legacy(db, aluno_id)
    if not aluno:
        logger.warning(f"Aluno ID {aluno_id} não encontrado.")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

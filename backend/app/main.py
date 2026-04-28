from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import List, Dict, Any
from datetime import datetime

from . import models, schemas
from .database import engine, get_db
from .pdf_parser import extract_pdf_data

models.Base.metadata.create_all(bind=engine)

# Configuração de Logs
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger("kannon_do_api")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "api.log"),
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = FastAPI(title="Kannon Do API Financeira")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        
        novos = []
        atualizados = []
        inalterados = []

        for rw in registros:
            aluno_info = rw["aluno"]
            mens_info = rw["mensalidade"]

            # Identificar aluno (Diferenciar pelo dependente para que pais com 2 filhos não mesclem matrículas)
            aluno_dependente = aluno_info.get("dependente")
            aluno_db = db.query(models.Aluno).filter(
                models.Aluno.nome_cliente == aluno_info["nome_cliente"],
                models.Aluno.dependente == aluno_dependente
            ).first()
            
            if not aluno_db:
                novos.append(rw)
                continue
            
            # Em caso de mesma data de vencimento (ex: linha inútil de 0,00 e a matrícula real), diferenciamos pelo Contrato
            # para não sobrepor faturas de pré-inscrição sobre as reais
            mensalidade_db = db.query(models.Mensalidade).filter(
                models.Mensalidade.aluno_id == aluno_db.id,
                models.Mensalidade.data_vencimento == mens_info["data_vencimento"],
                models.Mensalidade.contrato_num == mens_info["contrato_num"] # Nova segurança de isolamento
            ).first()

            if not mensalidade_db:
                # Nova mensalidade para aluno existente conta como novo registro (nova fatura)
                novos.append(rw)
            else:
                # Verifica se houve mudanca (status ou pagamentos)
                if (mensalidade_db.status != mens_info["status"] or 
                    mensalidade_db.valor_pago != mens_info["valor_pago"] or
                    mensalidade_db.data_pagamento != mens_info["data_pagamento"]):
                    
                    rw["_old_status"] = mensalidade_db.status
                    rw["_old_valor_pago"] = mensalidade_db.valor_pago
                    atualizados.append(rw)
                else:
                    inalterados.append(rw)
        
        return {
            "novos": novos,
            "atualizados": atualizados,
            "inalterados": inalterados,
            "total_encontrados": len(registros)
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)

@app.post("/upload-pdf-confirm/")
async def upload_pdf_confirm(registros: List[Dict[str, Any]] = Body(...), db: Session = Depends(get_db)):
    try:
        processados = 0
        logger.info(f"Confirmando processamento de {len(registros)} registros.")
        for rw in registros:
            aluno_info = rw["aluno"]
            mens_info = rw["mensalidade"]

            if isinstance(mens_info["data_vencimento"], str):
                mens_info["data_vencimento"] = datetime.fromisoformat(mens_info["data_vencimento"]).date()
            if mens_info.get("data_pagamento") and isinstance(mens_info["data_pagamento"], str):
                mens_info["data_pagamento"] = datetime.fromisoformat(mens_info["data_pagamento"]).date()

            aluno_dependente = aluno_info.get("dependente")
            aluno_db = db.query(models.Aluno).filter(
                models.Aluno.nome_cliente == aluno_info["nome_cliente"],
                models.Aluno.dependente == aluno_dependente
            ).first()
            if not aluno_db:
                aluno_db = models.Aluno(**aluno_info)
                db.add(aluno_db)
                db.commit()
                db.refresh(aluno_db)
            
            mensalidade_db = db.query(models.Mensalidade).filter(
                models.Mensalidade.aluno_id == aluno_db.id,
                models.Mensalidade.data_vencimento == mens_info["data_vencimento"],
                models.Mensalidade.contrato_num == mens_info["contrato_num"]
            ).first()

            if not mensalidade_db:
                nova_mensalidade = models.Mensalidade(**mens_info, aluno_id=aluno_db.id)
                db.add(nova_mensalidade)
            else:
                # Atualiza dados existentes
                mensalidade_db.status = mens_info["status"]
                mensalidade_db.valor_pago = mens_info["valor_pago"]
                mensalidade_db.data_pagamento = mens_info["data_pagamento"]
            
            processados += 1
        
        db.commit()
        return {"status": f"{processados} registros processados/atualizados com sucesso no banco!"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

@app.get("/alunos/")
def read_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alunos_db = db.query(models.Aluno).offset(skip).limit(limit).all()
    resultado = []
    
    for a in alunos_db:
        # Busca a mensalidade mais relevante: preferencialmente uma que tenha CONTRATO, 
        # senão pega a mais recente. Assim evitamos mostrar os 0,00 da pré-inscrição se a pessoa já for matriculada.
        mensalidades = db.query(models.Mensalidade).filter(models.Mensalidade.aluno_id == a.id).order_by(models.Mensalidade.data_vencimento.desc()).all()
        
        # Priorizar uma mensalidade que tenha contrato ou valor maior que zero. 
        # Isso garante que a pré-inscrição de valor 0,00 não ofusque a matrícula efetiva
        mensalidade_efetiva = next((m for m in mensalidades if m.contrato_num or m.valor_previsto > 0), None)
        ultima = mensalidade_efetiva if mensalidade_efetiva else (mensalidades[0] if mensalidades else None)
        
        teve_pre_inscricao = any(not m.contrato_num and m.valor_previsto == 0 for m in mensalidades) and len(mensalidades) > 1

        nome_exibicao = a.dependente if a.dependente else a.nome_cliente

        resultado.append({
            "id": a.id,
            "nome": nome_exibicao,
            "contrato": ultima.contrato_num if ultima and ultima.contrato_num else "S/N",
            "modalidade": ultima.mes_referencia if ultima and not ultima.contrato_num and ultima.valor_previsto > 0 else a.grupo_inscricao,
            "plano": "Mensal",
            "status": ultima.status if ultima else a.status_matricula,
            "valor": ultima.valor_previsto if ultima else 0.0,
            "pre_inscricao": teve_pre_inscricao
        })
        
    return resultado

@app.get("/alunos/{aluno_id}", response_model=schemas.AlunoComHistorico)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando detalhes do aluno ID: {aluno_id}")
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        logger.warning(f"Aluno ID {aluno_id} não encontrado.")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno
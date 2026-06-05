import os
os.environ["DISABLE_AUTH"] = "true"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from datetime import date

from app.main import app
from app.database import Base, get_db
from app.seed import seed_defaults

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_kannondo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        seed_defaults(db)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Kannon Do" in response.json()["message"]


def test_read_alunos_empty_initially():
    response = client.get("/alunos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch("app.main.extract_pdf_data")
def test_upload_pdf_preview_and_confirm(mock_extract):
    mock_data = [
        {
            "aluno": {
                "nome_cliente": "Aluno Teste 1",
                "dependente": None,
                "grupo_inscricao": "Kanon do/Geral",
                "status_matricula": "Ativa",
            },
            "mensalidade": {
                "contrato_num": "12345",
                "mes_referencia": "Jan/2026",
                "data_vencimento": date(2026, 1, 10),
                "data_pagamento": None,
                "valor_previsto": 150.0,
                "valor_pago": None,
                "taxa_bancaria": 1.99,
                "status": "Pendente",
            },
        }
    ]
    mock_extract.return_value = mock_data

    with open("mock.pdf", "w") as f:
        f.write("Mock file content")

    with open("mock.pdf", "rb") as f:
        resp_preview = client.post("/upload-pdf-preview/", files={"file": ("mock.pdf", f, "application/pdf")})

    import os as os_mod
    os_mod.remove("mock.pdf")

    assert resp_preview.status_code == 200
    data_preview = resp_preview.json()
    assert data_preview["total_encontrados"] == 1
    assert len(data_preview["novos"]) == 1

    resp_confirm = client.post("/upload-pdf-confirm/", json=data_preview["novos"])
    assert resp_confirm.status_code == 200
    assert "processados/atualizados com sucesso" in resp_confirm.json()["status"]

    resp_alunos = client.get("/alunos/")
    alunos = resp_alunos.json()
    assert len(alunos) >= 1
    assert alunos[0]["nome"] == "Aluno Teste 1"


def test_modalidades_list():
    resp = client.get("/modalidades/")
    assert resp.status_code == 200
    data = resp.json()
    slugs = [m["slug"] for m in data]
    assert "judo" in slugs
    assert "yoga" in slugs


def test_create_pessoa_and_cross_enrollment():
    resp_pessoa = client.post("/pessoas/", json={"nome": "Maria Silva", "email": "maria@test.com"})
    assert resp_pessoa.status_code == 200
    pessoa_id = resp_pessoa.json()["id"]

    modalidades = client.get("/modalidades/").json()
    judo_id = next(m["id"] for m in modalidades if m["slug"] == "judo")
    yoga_id = next(m["id"] for m in modalidades if m["slug"] == "yoga")

    turma_judo = client.post("/turmas/", json={"modalidade_id": judo_id, "nome": "Ter/Qui 20h"}).json()
    turma_yoga = client.post("/turmas/", json={"modalidade_id": yoga_id, "nome": "Sáb 10h"}).json()

    mat_judo = client.post("/matriculas/", json={"pessoa_id": pessoa_id, "turma_id": turma_judo["id"]})
    assert mat_judo.status_code == 200

    mat_yoga = client.post("/matriculas/", json={"pessoa_id": pessoa_id, "turma_id": turma_yoga["id"]})
    assert mat_yoga.status_code == 200

    matriculas = client.get(f"/pessoas/{pessoa_id}/matriculas").json()
    assert len(matriculas) == 2
    modalidades_nomes = {m["modalidade_nome"] for m in matriculas}
    assert "Judô" in modalidades_nomes
    assert "Yoga" in modalidades_nomes


def test_mensalidade_manual_and_metrics():
    pessoa = client.post("/pessoas/", json={"nome": "João Costa"}).json()
    modalidades = client.get("/modalidades/").json()
    yoga_id = next(m["id"] for m in modalidades if m["slug"] == "yoga")
    turma = client.post("/turmas/", json={"modalidade_id": yoga_id, "nome": "Dom 9h"}).json()
    matricula = client.post("/matriculas/", json={"pessoa_id": pessoa["id"], "turma_id": turma["id"]}).json()

    mens = client.post("/mensalidades/", json={
        "matricula_id": matricula["id"],
        "mes_referencia": "Jun/2026",
        "data_vencimento": "2026-06-10",
        "valor_previsto": 80.0,
        "status": "Pendente",
    })
    assert mens.status_code == 200

    metrics = client.get("/metrics/").json()
    assert metrics["total_pessoas"] >= 2
    assert metrics["receita_prevista"] >= 80.0
    assert len(metrics["por_modalidade"]) >= 2


def test_auth_login():
    resp = client.post("/auth/login", json={
        "email": "admin@kannondo.local",
        "password": "admin123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_migration_legacy():
    client.post("/pessoas/", json={"nome": "Migrar Test"})
    resp = client.post("/admin/migrate-legacy")
    assert resp.status_code == 200
    assert "alunos_processados" in resp.json()

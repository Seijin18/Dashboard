import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from unittest.mock import patch

# Banco de dados temporário em memória para testes isolados
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
    # Cria o banco
    Base.metadata.create_all(bind=engine)
    yield
    # Remove o banco depois dos testes
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Financeira Kannon Do rodando."}

def test_read_alunos_empty():
    response = client.get("/alunos/")
    assert response.status_code == 200
    assert response.json() == []

@patch("app.main.extract_pdf_data")
def test_upload_pdf_preview_and_confirm(mock_extract):
    from datetime import date
    
    # Criaremos um mock do que o PDF devolve
    mock_data = [
        {
            "aluno": {
                "nome_cliente": "Aluno Teste 1",
                "dependente": None,
                "grupo_inscricao": "Kanon do/Geral",
                "status_matricula": "Ativa"
            },
            "mensalidade": {
                "contrato_num": "12345",
                "mes_referencia": "Jan/2026",
                "data_vencimento": date(2026, 1, 10),
                "data_pagamento": None,
                "valor_previsto": 150.0,
                "valor_pago": None,
                "taxa_bancaria": 1.99,
                "status": "Pendente"
            }
        }
    ]
    mock_extract.return_value = mock_data

    # A - Enviar um arquivo mock para abrir a Prévia
    with open("mock.pdf", "w") as f:
        f.write("Mock file content")
        
    with open("mock.pdf", "rb") as f:
        # Pre-visualização de Aluno 100% Novo
        resp_preview = client.post("/upload-pdf-preview/", files={"file": ("mock.pdf", f, "application/pdf")})
    
    import os
    os.remove("mock.pdf")
    
    assert resp_preview.status_code == 200
    data_preview = resp_preview.json()
    assert data_preview["total_encontrados"] == 1
    assert len(data_preview["novos"]) == 1
    assert len(data_preview["atualizados"]) == 0
    assert len(data_preview["inalterados"]) == 0
    
    # B - O Usuário dá o Confirm no frontend, com os JSONs misturados
    payload = data_preview["novos"]
    
    resp_confirm = client.post("/upload-pdf-confirm/", json=payload)
    assert resp_confirm.status_code == 200
    assert "processados/atualizados com sucesso" in resp_confirm.json()["status"]

    # C - Ver se inseriu no banco GET /alunos/
    resp_alunos = client.get("/alunos/")
    assert resp_alunos.status_code == 200
    alunos = resp_alunos.json()
    assert len(alunos) == 1
    assert alunos[0]["nome"] == "Aluno Teste 1"
    assert alunos[0]["contrato"] == "12345"
    assert alunos[0]["status"] == "Pendente"
    assert alunos[0]["valor"] == 150.0

@patch("app.main.extract_pdf_data")
def test_upload_pdf_atualizacao(mock_extract):
    from datetime import date
    
    # Agindo como se outro arquivo viesse no mês seguinte ou com fatura Paga
    mock_data_atualizado = [
        {
            "aluno": {
                "nome_cliente": "Aluno Teste 1",
                "dependente": None,
                "grupo_inscricao": "Kanon do/Geral",
                "status_matricula": "Ativa"
            },
            "mensalidade": {
                "contrato_num": "12345",
                "mes_referencia": "Jan/2026",
                "data_vencimento": date(2026, 1, 10),
                "data_pagamento": date(2026, 1, 11),
                "valor_previsto": 150.0,
                "valor_pago": 150.0,
                "taxa_bancaria": 1.99,
                "status": "Pago"
            }
        }
    ]
    mock_extract.return_value = mock_data_atualizado

    with open("mock.pdf", "w") as f: f.write("Mock file")
    with open("mock.pdf", "rb") as f:
        resp_preview = client.post("/upload-pdf-preview/", files={"file": ("mock.pdf", f, "application/pdf")})
    import os
    os.remove("mock.pdf")
    
    data_preview = resp_preview.json()
    
    # Como era uma data igual, o banco reconhece o aluno.
    # Como o valor pago e status passaram de Pendente e None pra Pago e 150, é uma ATUALIZAÇÃO!
    assert len(data_preview["atualizados"]) == 1
    assert data_preview["atualizados"][0]["_old_status"] == "Pendente"
    assert data_preview["atualizados"][0]["mensalidade"]["status"] == "Pago"
    
    # Confirmação da alteração
    payload = data_preview["atualizados"]
    resp_confirm = client.post("/upload-pdf-confirm/", json=payload)
    assert resp_confirm.status_code == 200
    
    # GET /alunos/
    resp_alunos = client.get("/alunos/")
    alunos = resp_alunos.json()
    assert alunos[0]["status"] == "Pago" # Foi atualizado!


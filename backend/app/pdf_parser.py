import pdfplumber
import re
from datetime import datetime

def parse_currency(value_str):
    if not value_str:
        return 0.0
    cleaned = re.sub(r'[^0-9,]', '', value_str)
    if not cleaned: return 0.0
    return float(cleaned.replace(',', '.'))

def extract_pdf_data(file_path: str):
    """
    Extrai dados do PDF report do sistema Galileu lendo o texto bruto de forma precisa as instruções.
    """
    extracted_data = []
    
    with pdfplumber.open(file_path) as pdf:
        text = '\n'.join(p.extract_text() for p in pdf.pages if p.extract_text())
        
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Regex para achar a primeira linha do bloco da fatura
        # (Cliente) (Grupo) (Situação) (Vencimento) (Vlr_Prev) (Vlr Ate_Venc) [Dt_Pag] [Vlr_Pago]?
        m = re.search(r'^(.*?)\s+(PRÉ - Inscrição|Mensalidade)\s+(Quitado|Pendente|Vencido)\s+(\d{2}/\d{2}/\d{4})\s+(R\$ [\d.,]+)\s+(R\$ [\d.,]+)(?:\s+(\d{2}/\d{2}/\d{4}))?(?:\s+(R\$ [\d.,]+))?$', line)
        
        if m:
            nome_cliente = m.group(1).strip()
            grupo_linha_1 = m.group(2).strip()
            situacao = m.group(3).strip()
            vencimento_str = m.group(4)
            valor_prev = parse_currency(m.group(5))
            pagamento_str = m.group(7)
            valor_pago = parse_currency(m.group(8)) if m.group(8) else 0.0
            
            dependente = None
            contrato_num = None
            mes_referencia = "Mensal"
            turma_extraida = "Kannon Do"
            
            if i + 2 < len(lines):
                desc_line = lines[i+1] + " " + lines[i+2] + " " + (lines[i+3] if i+3 < len(lines) else "")
                
                dep_match = re.search(r'([A-Za-zÀ-ÿ\s]+?)\s+\(\d+/\d+\)', lines[i+2])
                if dep_match:
                    dependente = dep_match.group(1).strip()
                else:
                    dependente = lines[i+2].split('CONTRATO')[0].split('PRÉ -')[0].strip()

                # Extrai a turma/localização
                tm = re.search(r'(?:Kanon|Kannon)\s*do\s*/\s*([A-Za-zçã]+\s*e\s*[A-Za-z]+\s*\d{2}h\d{0,2})', desc_line, re.IGNORECASE)
                if tm:
                    turma_extraida = f"Kannon Do / {tm.group(1).strip()}"
                else:
                    tm2 = re.search(r'([A-Za-zçã]+\s*e\s*[A-Za-z]+\s*\d{2}h\d{0,2})', desc_line, re.IGNORECASE)
                    if tm2:
                        turma_extraida = tm2.group(1).strip()
                
                # Extrai o contrato
                mc = re.search(r'CONTRATO(?:S)?\s*(?:Nº|N|#)?\s*(\d+)', desc_line, re.IGNORECASE)
                if mc: contrato_num = mc.group(1)
                
                # Extrai o mês na Mensalidade (e.g. Abril/2026)
                mm = re.search(r'Mensalidade[^\n]*?([A-Za-z]+/\d{4})', desc_line, re.IGNORECASE)
                if mm: 
                    mes_referencia = mm.group(1)
                elif grupo_linha_1 == "PRÉ - Inscrição":
                    mes_referencia = "Pré-inscrição"
                
            vencimento = datetime.strptime(vencimento_str.strip(), '%d/%m/%Y').date()
            pagamento = datetime.strptime(pagamento_str.strip(), '%d/%m/%Y').date() if pagamento_str else None
            
            extracted_data.append({
                "aluno": {
                    "nome_cliente": nome_cliente,
                    "dependente": dependente if dependente and dependente != nome_cliente else None,
                    "grupo_inscricao": turma_extraida,  # Alterado para espelhar a "turma" do descritivo
                    "status_matricula": "Ativa"
                },
                "mensalidade": {
                    "contrato_num": contrato_num,
                    "mes_referencia": mes_referencia,
                    "data_vencimento": vencimento,
                    "data_pagamento": pagamento,
                    "valor_previsto": valor_prev,
                    "valor_pago": valor_pago if situacao == "Quitado" else None,
                    "taxa_bancaria": 1.99,
                    "status": situacao
                }
            })
            
            i += 2 # pula as próximas linhas lidas
        else:
            i += 1
            
    return extracted_data
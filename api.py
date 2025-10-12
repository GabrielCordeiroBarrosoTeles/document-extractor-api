from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import json
import os
import shutil
from datetime import datetime
from extractor import DocumentExtractor
from typing import List
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do .env
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8080))
API_TITLE = os.getenv("API_TITLE", "API Extrator de Documentos")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
JSON_FILE = os.getenv("JSON_FILE", "documentos_processados.json")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

app = FastAPI(title=API_TITLE, version=API_VERSION)
extractor = DocumentExtractor()

os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_json_data():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json_data(data):
    """Salva dados no arquivo JSON"""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/")
async def root():
    return {"message": "API Extrator de Documentos - Envie arquivos via POST /processar"}

@app.post("/processar")
async def processar_documento(file: UploadFile = File(...)):
    """Processa um documento e extrai informações"""
    
    # Verifica se é uma imagem ou PDF
    allowed_types = ['image/', 'application/pdf']
    if not any(file.content_type.startswith(t) for t in allowed_types):
        raise HTTPException(status_code=400, detail="Apenas arquivos de imagem e PDF são aceitos")
    
    try:
        # Salva o arquivo temporariamente
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Processa o documento
        resultado = extractor.process_document(file_path)
        
        # Carrega dados existentes
        dados = load_json_data()
        
        # Adiciona novo resultado
        resultado["id"] = len(dados) + 1
        dados.append(resultado)
        
        # Salva no JSON
        save_json_data(dados)
        
        # Remove arquivo temporário
        os.remove(file_path)
        
        return JSONResponse(content=resultado)
        
    except Exception as e:
        # Remove arquivo temporário em caso de erro
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}")

@app.get("/documentos")
async def listar_documentos():
    """Lista todos os documentos processados"""
    dados = load_json_data()
    return {"total": len(dados), "documentos": dados}

@app.get("/documentos/{doc_id}")
async def obter_documento(doc_id: int):
    """Obtém um documento específico pelo ID"""
    dados = load_json_data()
    
    for doc in dados:
        if doc.get("id") == doc_id:
            return doc
    
    raise HTTPException(status_code=404, detail="Documento não encontrado")

@app.get("/estatisticas")
async def obter_estatisticas():
    """Obtém estatísticas dos documentos processados"""
    dados = load_json_data()
    
    if not dados:
        return {"total": 0, "categorias": {}, "valor_total": 0}
    
    categorias = {}
    valor_total = 0
    
    for doc in dados:
        categoria = doc.get("categoria", "outros")
        categorias[categoria] = categorias.get(categoria, 0) + 1
        
        if doc.get("valor_total"):
            valor_total += doc["valor_total"]
    
    return {
        "total_documentos": len(dados),
        "categorias": categorias,
        "valor_total": valor_total,
        "valor_medio": valor_total / len(dados) if dados else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=DEBUG)
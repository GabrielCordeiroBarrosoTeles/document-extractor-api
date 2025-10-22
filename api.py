from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from datetime import datetime
from extractor import DocumentExtractor
from database import DatabaseManager
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
db = DatabaseManager()

os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        resultado["nome_arquivo"] = file.filename
        
        # Salva no banco
        doc_id = db.save_document(resultado)
        resultado["id"] = doc_id
        
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
    dados = db.get_all_documents()
    return {"total": len(dados), "documentos": dados}

@app.get("/documentos/{doc_id}")
async def obter_documento(doc_id: int):
    """Obtém um documento específico pelo ID"""
    documento = db.get_document_by_id(doc_id)
    
    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    
    return documento

@app.get("/estatisticas")
async def obter_estatisticas():
    """Obtém estatísticas dos documentos processados"""
    return db.get_statistics()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=DEBUG)
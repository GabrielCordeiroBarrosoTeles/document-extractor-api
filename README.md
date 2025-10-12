# API Extrator de Documentos 🤖

IA em Python para extrair informações de comprovantes de pagamento e boletos usando OCR.

## 🏗️ Arquitetura

```mermaid
flowchart LR
    A[Upload] --> B[OCR]
    B --> C[Extração]
    C --> D[Classificação]
    D --> E[JSON]
```

## 🚀 Funcionalidades

- **OCR**: Extrai texto de PDFs e imagens
- **Dados**: Datas, valores e beneficiários
- **Categorias**: 25+ tipos automáticos
- **API REST**: 3 endpoints principais

## 🚀 Uso Rápido

```bash
# Instalar
pip install -r requirements.txt
brew install tesseract tesseract-lang
cp .env.example .env

# Executar
python api.py

# Testar
open http://localhost:8080/docs
```

## 📡 Endpoints

- `POST /processar` - Processar documento
- `GET /documentos` - Listar documentos
- `GET /estatisticas` - Ver estatísticas

## 📊 Resposta

```json
{
  "data_vencimento": "15/01/2024",
  "valor_total": 150.50,
  "categoria": "educacao",
  "beneficiario": "Universidade XYZ"
}
```

## 🎯 Categorias (25+)

Educação • Treino • Delivery • Saúde • Transporte • Alimentação • Moradia • Vestuário • Lazer • Tecnologia • Serviços • Pets • Beleza • Casa • Investimentos • Trabalho • Impostos • Doação • Assinaturas • Emergência • Jurídico • Comunicação • Cultura • Esportes • Infantil

## 📁 Estrutura

```
├── api.py              # FastAPI
├── extractor.py        # OCR Logic
├── requirements.txt    # Dependencies
├── .env.example       # Config
└── uploads/           # Files
```

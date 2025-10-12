# API Extrator de Documentos 🤖

<<<<<<< HEAD
IA em Python para extrair informações de comprovantes de pagamento e boletos usando OCR.
=======
IA em Python para extrair informações de comprovantes de pagamento e boletos.
>>>>>>> 7c52dc7ba4a0802a6b978a257adcabbb1c560690

## 🏗️ Arquitetura

```mermaid
<<<<<<< HEAD
flowchart LR
    A[Upload] --> B[OCR]
    B --> C[Extração]
    C --> D[Classificação]
    D --> E[JSON]
=======
flowchart TD
    A[Cliente] --> B[FastAPI Server]
    B --> C{Tipo de Arquivo?}
    
    C -->|PDF| D[PDF Text Extract]
    C -->|Imagem| E[Image Preprocessing]
    
    D --> F[PyMuPDF]
    D --> G[PDF2Image + OCR]
    E --> H[OpenCV]
    H --> I[Tesseract OCR]
    
    F --> J[Texto Extraído]
    G --> J
    I --> J
    
    J --> K[DocumentExtractor]
    K --> L[Extração de Datas]
    K --> M[Extração de Valores]
    K --> N[Extração de Beneficiário]
    K --> O[Classificação por Categoria]
    
    O --> P[25+ Categorias]
    
    L --> Q[Resultado JSON]
    M --> Q
    N --> Q
    P --> Q
    
    Q --> R[documentos_processados.json]
    Q --> S[Resposta API]
    S --> A
    
    T[uploads/] --> C
    
    subgraph "Endpoints"
        U[POST /processar]
        V[GET /documentos]
        W[GET /estatisticas]
    end
    
    B --> U
    B --> V
    B --> W
>>>>>>> 7c52dc7ba4a0802a6b978a257adcabbb1c560690
```

## 🚀 Funcionalidades

<<<<<<< HEAD
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
=======
- **Extração de dados via OCR**: Data de vencimento, data de pagamento, valor total
- **Classificação automática**: Educação, treino, delivery, saúde, transporte, alimentação
- **API REST**: Endpoints para processar e consultar documentos
- **Armazenamento JSON**: Salva todas as informações extraídas

## 📋 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar Tesseract OCR (macOS)
brew install tesseract tesseract-lang

# Ou no Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

## 🔧 Como usar

### 1. Iniciar a API
```bash
python api.py
```

### 2. Acessar interface
- Swagger UI: http://localhost:8080/docs
- API: http://localhost:8080

### 3. Endpoints disponíveis

- `POST /processar` - Enviar documento para processamento
- `GET /documentos` - Listar todos os documentos
- `GET /documentos/{id}` - Obter documento específico
- `GET /estatisticas` - Ver estatísticas dos documentos

### 4. Testar
- Acesse http://localhost:8080/docs
- Use a interface Swagger para enviar arquivos

## 📊 Exemplo de resposta

```json
{
  "id": 1,
  "arquivo": "comprovante.jpg",
  "data_processamento": "2024-01-15T10:30:00",
  "data_vencimento": "15/01/2024",
  "data_pagamento": "14/01/2024",
  "valor_total": 150.50,
  "categoria": "educacao",
  "beneficiario": "Universidade XYZ",
  "texto_extraido": "Comprovante de pagamento..."
}
```

## 🎯 Categorias suportadas (25+ categorias)

- **Educação**: escola, universidade, curso, faculdade, pós-graduação, idiomas
- **Treino**: academia, personal, fitness, pilates, yoga, natação, boxe, dança
- **Delivery**: ifood, uber eats, rappi, james delivery, aiqfome, 99food
- **Saúde**: plano de saúde, médico, hospital, farmácia, exames, psicologia
- **Transporte**: uber, taxi, combustível, metrô, ônibus, estacionamento, IPVA
- **Alimentação**: supermercado, restaurante, padaria, bar, cafeteria, feira
- **Moradia**: aluguel, condomínio, IPTU, água, luz, gás, internet, TV cabo
- **Vestuário**: roupas, calçados, acessórios, bolsas, joias, óculos
- **Lazer**: cinema, teatro, shows, viagens, hotéis, eventos, museus
- **Tecnologia**: celular, computador, software, streaming, apps, iCloud
- **Serviços**: banco, cartão, seguros, advocacia, contabilidade, correios
- **Pets**: veterinário, pet shop, ração, vacinas, tosa, hotel para pets
- **Beleza**: salão, barbeiro, estética, cosméticos, spa, depilação
- **Casa**: móveis, decoração, eletrodomésticos, ferramentas, reforma
- **Investimentos**: corretora, ações, fundos, previdência, cripto, CDB
- **Trabalho**: material escritório, papelaria, coworking, treinamentos
- **Impostos**: IPTU, IPVA, IR, taxas, multas, DARF
- **Doação**: caridade, ONGs, igreja, dízimo, beneficência
- **Assinaturas**: mensalidades, anuidades, premium, recorrentes
- **Emergência**: hospital, ambulância, socorro, chaveiro, guincho
- **Jurídico**: advogado, processos, cartório, documentação
- **Comunicação**: telefone, internet, TV, jornal, revista
- **Cultura**: livros, arte, biblioteca, fotografia, design
- **Esportes**: futebol, tênis, corrida, bicicleta, competições
- **Infantil**: brinquedos, creche, fraldas, pediatra, escola infantil

## 📁 Estrutura do projeto

```
apiDocumento/
├── api.py              # API FastAPI
├── extractor.py        # Lógica de extração OCR
├── requirements.txt    # Dependências
├── .env               # Configurações
├── .gitignore         # Arquivos ignorados
├── start.sh           # Script para iniciar
├── uploads/           # Arquivos temporários
└── documentos_processados.json  # Banco de dados JSON
>>>>>>> 7c52dc7ba4a0802a6b978a257adcabbb1c560690
```
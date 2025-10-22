#!/bin/bash

echo "🚀 Iniciando Document Extractor API com MySQL..."

# Cria arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
fi

# Cria diretório uploads se não existir
mkdir -p uploads

# Inicia os containers
echo "🐳 Iniciando containers Docker..."
docker-compose up -d

echo "⏳ Aguardando MySQL inicializar..."
sleep 10

echo "✅ API disponível em: http://localhost:8080"
echo "📚 Documentação em: http://localhost:8080/docs"
echo "🗄️  MySQL rodando na porta 3306"

# Mostra logs
echo "📋 Logs da API:"
docker-compose logs -f api
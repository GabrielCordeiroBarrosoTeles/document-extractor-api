CREATE TABLE IF NOT EXISTS documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_arquivo VARCHAR(255),
    data_vencimento DATE,
    valor_total DECIMAL(10,2),
    categoria VARCHAR(100),
    beneficiario VARCHAR(255),
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    texto_extraido TEXT,
    confianca DECIMAL(3,2)
);
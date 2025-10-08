-- Primeiro, criar o tipo enumerado se ainda não existir
CREATE TYPE tipo_usuario AS ENUM ('ADMIN', 'FISCAL', 'USER');

-- Criar a tabela usuario
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario tipo_usuario DEFAULT 'USER',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índice no email para melhor performance nas consultas
CREATE INDEX idx_usuario_email ON usuario(email);

-- Criar índice no campo is_active para consultas filtradas
CREATE INDEX idx_usuario_is_active ON usuario(is_active);
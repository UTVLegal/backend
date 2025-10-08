CREATE TABLE carro (
    id SERIAL PRIMARY KEY,
    cpf_piloto VARCHAR(11) NOT NULL REFERENCES piloto(cpf_piloto) ON DELETE CASCADE,
    foto_frente BYTEA NOT NULL,
    foto_tras BYTEA NOT NULL,
    foto_esquerda BYTEA NOT NULL,
    foto_direita BYTEA NOT NULL,
    nota_fiscal BYTEA NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
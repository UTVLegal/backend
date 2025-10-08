CREATE TYPE tipo_endereco AS ENUM (
    'RESIDENCIAL',
    'COMERCIAL',
    'OUTRO'
);

CREATE TYPE uf_brasil AS ENUM (
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
    'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
    'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
);

-- Criar a tabela endereco
CREATE TABLE endereco (
    id SERIAL PRIMARY KEY,
    cpf_piloto VARCHAR(11) NOT NULL REFERENCES piloto(cpf_piloto) ON DELETE CASCADE,
    tipo_endereco tipo_endereco NOT NULL,
    cep VARCHAR(10) NOT NULL,
    logradouro VARCHAR(100) NOT NULL,
    numero INTEGER,
    complemento VARCHAR(50),
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    uf uf_brasil NOT NULL,
    pais VARCHAR(30) DEFAULT 'Brasil' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar a função para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para atualizar updated_at automaticamente
CREATE TRIGGER trigger_update_updated_at
    BEFORE UPDATE ON endereco
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Criar índices para melhor performance
CREATE INDEX idx_endereco_cpf_piloto ON endereco(cpf_piloto);
CREATE INDEX idx_endereco_cep ON endereco(cep);
CREATE INDEX idx_endereco_cidade ON endereco(cidade);
CREATE INDEX idx_endereco_uf ON endereco(uf);
CREATE INDEX idx_endereco_tipo ON endereco(tipo_endereco);
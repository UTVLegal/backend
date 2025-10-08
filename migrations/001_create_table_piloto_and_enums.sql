CREATE TYPE estado_civil AS ENUM (
  'SOLTEIRO',
  'CASADO',
  'VIUVO',
  'OUTROS'
);

CREATE TYPE tipo_sanguineo AS ENUM (
  'A_POSITIVO',
  'A_NEGATIVO',
  'B_POSITIVO',
  'B_NEGATIVO',
  'AB_POSITIVO',
  'AB_NEGATIVO',
  'O_POSITIVO',
  'O_NEGATIVO'
);

CREATE TABLE piloto (
  cpf_piloto VARCHAR(11) PRIMARY KEY,
  nome_piloto VARCHAR(255) NOT NULL,
  email_piloto VARCHAR(255) UNIQUE NOT NULL,
  numero_telefone VARCHAR(20) UNIQUE NOT NULL,
  estado_civil estado_civil NOT NULL,
  nome_contato_seguranca VARCHAR(255) NOT NULL,
  numero_contato_seguranca VARCHAR(20) NOT NULL,
  tipo_sanguineo tipo_sanguineo NOT NULL,
  nome_plano_saude VARCHAR(255) NOT NULL,
  foto_cnh BYTEA,
  foto_cnh_tipo VARCHAR(100),
  foto_piloto BYTEA,
  foto_piloto_tipo VARCHAR(100),
  id_piloto VARCHAR(100),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  data_nascimento DATE NOT NULL
);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
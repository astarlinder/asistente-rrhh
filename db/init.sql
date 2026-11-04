CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documentos (
    id          SERIAL PRIMARY KEY,
    nombre      TEXT NOT NULL UNIQUE,
    cargado_en  TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fragmentos (
    id            SERIAL PRIMARY KEY,
    documento_id  INTEGER NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
    pagina        INTEGER NOT NULL,
    texto         TEXT NOT NULL,
    embedding     vector(384)
);

CREATE INDEX IF NOT EXISTS idx_fragmentos_embedding
    ON fragmentos USING hnsw (embedding vector_cosine_ops);
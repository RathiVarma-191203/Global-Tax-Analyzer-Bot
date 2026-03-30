"""
Script to create the missing document_chunks table using properly URL-encoded connection params.
"""
import sys
import subprocess

SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE TABLE IF NOT EXISTS public.document_chunks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    document_id UUID REFERENCES public.documents(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(384)
);

CREATE INDEX IF NOT EXISTS idx_chunks_user_id ON public.document_chunks(user_id);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON public.document_chunks USING hnsw (embedding vector_cosine_ops);

ALTER TABLE public.document_chunks ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename='document_chunks' 
        AND policyname='Users can CRUD own chunks'
    ) THEN
        CREATE POLICY "Users can CRUD own chunks" ON public.document_chunks FOR ALL USING (auth.uid() = user_id);
    END IF;
END$$;

CREATE OR REPLACE FUNCTION match_document_chunks (
  query_embedding VECTOR(384),
  match_threshold FLOAT,
  match_count INT,
  p_user_id UUID
)
RETURNS TABLE (
  id UUID,
  document_id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.id,
    dc.document_id,
    dc.content,
    dc.metadata,
    1 - (dc.embedding <=> query_embedding) AS similarity
  FROM public.document_chunks dc
  WHERE dc.user_id = p_user_id
    AND 1 - (dc.embedding <=> query_embedding) > match_threshold
  ORDER BY dc.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
"""

def run():
    try:
        import psycopg2
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], check=True)
        import psycopg2

    # URL-encode the @ in password using individual parameters
    print("Connecting to Supabase PostgreSQL...")
    conn = psycopg2.connect(
        host="aws-1-ap-northeast-1.pooler.supabase.com",
        port=6543,
        dbname="postgres",
        user="postgres.uthyxhcovkcfkjtsyxoc",
        password="Varma@191203",
        sslmode="require"
    )
    conn.autocommit = True
    cur = conn.cursor()
    print("Running schema migration...")
    cur.execute(SQL)
    print("✅ Schema applied successfully!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    run()

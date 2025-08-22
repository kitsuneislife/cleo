# Memory service — Interface

APIs
- POST /memory/store {"id", "embedding", "metadata"}
- POST /memory/query {"query_embedding", "top_k":10}

Data store
- Use a vector DB compatible format (FAISS locally, Pinecone/Weaviate in cloud).
- Metadata must avoid PII; enforce sanitization upstream.

MVP
- store, query, delete by id, simple TTL-based retention.

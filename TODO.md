# TODO

- Ecocardiograma: generar PDF real (WeasyPrint) como carótidas.
- Ecocardiograma: ocultar secciones vacías en impresión PDF.
- RAG: agregar PDF de carótidas legacy y cualquier otro PDF faltante a `Scrap_cardioprietohc/data/raw/`.
- RAG: reindexar si se agregan nuevos PDFs o HTML (`python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`).

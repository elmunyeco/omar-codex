import argparse
from pathlib import Path

from .client import ScrapClient
from .crawlers.historias import scrape_historias
from .crawlers.pacientes import scrape_pacientes
from .rag import RagIndex, build_index


def _cmd_run(target: str):
    client = ScrapClient()
    if not client.base_url:
        raise SystemExit("BASE_URL no configurada (.env).")
    if not client.login():
        raise SystemExit("Login falló; revisá credenciales o endpoint")

    if target == "pacientes":
        scrape_pacientes(client)
    elif target == "historias":
        scrape_historias(client)

    client.close()


def _cmd_rag_index(source: Path, index_path: Path, glob: str, max_features: int):
    saved = build_index(source_dir=source, index_path=index_path, glob=glob, max_features=max_features)
    print(f"Índice guardado en {saved}")


def _cmd_rag_query(index_path: Path, query: str, top_k: int):
    idx = RagIndex.load(index_path)
    results = idx.query(query, top_k=top_k)
    for r in results:
        print(f"[{r.score:.3f}] {r.source} :: {r.fragment}")


def main():
    parser = argparse.ArgumentParser(description="Scraper cardioprietohc")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Ejecuta scraping por módulo")
    run_cmd.add_argument("--target", choices=["pacientes", "historias"], required=True)

    idx_cmd = sub.add_parser("rag-index", help="Construye índice TF-IDF sobre data/raw")
    idx_cmd.add_argument("--source", type=Path, default=Path("data/raw"))
    idx_cmd.add_argument("--index", type=Path, default=Path("data/cache/rag_index.pkl"))
    idx_cmd.add_argument("--glob", default="*")
    idx_cmd.add_argument("--max-features", type=int, default=5000)

    query_cmd = sub.add_parser("rag-query", help="Consulta índice TF-IDF")
    query_cmd.add_argument("--index", type=Path, default=Path("data/cache/rag_index.pkl"))
    query_cmd.add_argument("--query", required=True)
    query_cmd.add_argument("--top-k", type=int, default=5)

    args = parser.parse_args()

    if args.command == "run":
        _cmd_run(target=args.target)
    elif args.command == "rag-index":
        _cmd_rag_index(source=args.source, index_path=args.index, glob=args.glob, max_features=args.max_features)
    elif args.command == "rag-query":
        _cmd_rag_query(index_path=args.index, query=args.query, top_k=args.top_k)


if __name__ == "__main__":
    main()

import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RagResult:
    score: float
    source: str
    fragment: str


def _chunk_text(text: str, max_len: int = 800) -> List[str]:
    """Divide texto en bloques legibles sin cortar demasiado."""
    words = text.split()
    chunks: List[str] = []
    buf: List[str] = []
    length = 0
    for w in words:
        buf.append(w)
        length += len(w) + 1
        if length >= max_len:
            chunks.append(" ".join(buf))
            buf = []
            length = 0
    if buf:
        chunks.append(" ".join(buf))
    return chunks


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Elimina scripts/estilos para evitar ruido.
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def _json_to_text(data: Iterable[Dict]) -> str:
    return json.dumps(data, ensure_ascii=False)


def build_index(
    source_dir: Path,
    index_path: Path,
    glob: str = "*",
    max_features: int = 5000,
) -> Path:
    """Crea un índice TF-IDF simple sobre los archivos de `source_dir`."""
    documents: List[Dict[str, str]] = []
    for file_path in sorted(Path(source_dir).rglob(glob)):
        if not file_path.is_file():
            continue
        text = ""
        if file_path.suffix.lower() in {".html", ".htm"}:
            text = _html_to_text(file_path.read_text(encoding="utf-8"))
        elif file_path.suffix.lower() == ".json":
            text = _json_to_text(json.loads(file_path.read_text(encoding="utf-8")))
        else:
            # Otros textos simples.
            text = file_path.read_text(encoding="utf-8", errors="ignore")

        for chunk in _chunk_text(text):
            documents.append(
                {
                    "text": chunk,
                    "source": str(file_path.relative_to(source_dir)),
                }
            )

    if not documents:
        raise ValueError(f"No se encontraron documentos en {source_dir}")

    corpus = [d["text"] for d in documents]
    vectorizer = TfidfVectorizer(max_features=max_features)
    matrix = vectorizer.fit_transform(corpus)

    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("wb") as f:
        pickle.dump(
            {
                "vectorizer": vectorizer,
                "matrix": matrix,
                "documents": documents,
            },
            f,
        )
    return index_path


class RagIndex:
    def __init__(self, vectorizer, matrix, documents: Sequence[Dict[str, str]]):
        self.vectorizer = vectorizer
        self.matrix = matrix
        self.documents = documents

    @classmethod
    def load(cls, index_path: Path) -> "RagIndex":
        with index_path.open("rb") as f:
            data = pickle.load(f)
        return cls(data["vectorizer"], data["matrix"], data["documents"])

    def query(self, text: str, top_k: int = 5) -> List[RagResult]:
        if not text.strip():
            return []
        vec = self.vectorizer.transform([text])
        sims = cosine_similarity(vec, self.matrix).ravel()
        order = sims.argsort()[::-1][:top_k]
        return [
            RagResult(
                score=float(sims[i]),
                source=self.documents[i]["source"],
                fragment=self.documents[i]["text"][:400],
            )
            for i in order
        ]

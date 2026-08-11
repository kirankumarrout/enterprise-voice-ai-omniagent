from pathlib import Path
import re
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGEngine:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.rebuild()

    def _read(self, path):
        if path.suffix.lower() == ".pdf":
            return "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
        return path.read_text(encoding="utf-8", errors="ignore")

    def rebuild(self):
        self.chunks = []
        for path in self.data_dir.glob("*"):
            if path.suffix.lower() not in {".txt", ".md", ".pdf"}:
                continue
            text = re.sub(r"\s+", " ", self._read(path)).strip()
            start = 0
            while start < len(text):
                end = min(start + 900, len(text))
                chunk = text[start:end].strip()
                if chunk:
                    self.chunks.append({"text": chunk, "source": path.name})
                if end >= len(text):
                    break
                start = end - 150
        if self.chunks:
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
            self.matrix = self.vectorizer.fit_transform([x["text"] for x in self.chunks])
        else:
            self.vectorizer = self.matrix = None

    def search(self, query, k=4):
        if not self.matrix:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        ids = scores.argsort()[::-1][:k]
        return [{"text": self.chunks[i]["text"], "source": self.chunks[i]["source"],
                 "score": round(float(scores[i]), 4)}
                for i in ids if scores[i] > 0]

    def add_file(self, filename, content):
        path = self.data_dir / Path(filename).name
        path.write_bytes(content)
        self.rebuild()
        return path.name

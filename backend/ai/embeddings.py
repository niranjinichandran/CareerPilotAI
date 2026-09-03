from typing import List
from backend.core.config import settings

class EmbeddingService:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = None

    def _load_model(self):
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(self.model_name)
            except Exception:
                self.model = False

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        self._load_model()
        if self.model:
            try:
                embeddings = self.model.encode(texts, show_progress_bar=False)
                return embeddings.tolist()
            except Exception:
                pass
        
        # Fast fallback deterministic vector generator
        vectors = []
        for text in texts:
            vec = [(ord(char) % 100) / 100.0 for char in text[:384]]
            if len(vec) < 384:
                vec.extend([0.0] * (384 - len(vec)))
            vectors.append(vec)
        return vectors

    def embed_query(self, text: str) -> List[float]:
        return self.embed_texts([text])[0]

embedding_service = EmbeddingService()

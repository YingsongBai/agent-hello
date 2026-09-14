from typing import Optional

from langchain_huggingface import HuggingFaceEndpointEmbeddings
from qdrant_client import QdrantClient

from app.conf.app_config import EmbeddingConfig, app_config, QdrantConfig
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct


class QdrantClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: QdrantConfig|None = None
        self.config: QdrantConfig = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = QdrantClient(url=self._get_url())

    def close(self):
        self.client.close()


embedding_client_manager = QdrantClientManager(app_config.embedding)


if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )


    operation_info = client.upsert(
        collection_name="test_collection",
        wait=True,
        points=[
            PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
            PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
            PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
            PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
            PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
            PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
        ],
    )
    search_result = client.query_points(
        collection_name="test_collection",
        query=[0.2, 0.1, 0.9, 0.7],
        with_payload=False,
        limit=3
    ).points

    print(search_result)

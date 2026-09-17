from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.conf.app_config import EmbeddingConfig, app_config
from huggingface_hub import InferenceClient


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: InferenceClient | None = None
        self.config = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = InferenceClient(base_url=self._get_url())


embedding_client_manager = EmbeddingClientManager(app_config.embedding)

if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client
    text = 'what is deep learning?'
    query_result = client.feature_extraction(text)
    print(query_result[0][:5])

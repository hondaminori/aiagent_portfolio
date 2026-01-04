from langchain_openai import OpenAIEmbeddings

def create_embedding(api_key: str, embedding_model_name: str) -> OpenAIEmbeddings:
    """
    OpenAI Embedding オブジェクトを生成する。
    """
    embedding = OpenAIEmbeddings(
        model=embedding_model_name,
        api_key=api_key
    )

    return embedding

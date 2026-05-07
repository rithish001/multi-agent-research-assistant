import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

#Persistent client
client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = OllamaEmbeddingFunction(model_name="qwen2.5:0.5b")

collection=client.get_or_create_collection(
    name="research_memory",
    embedding_function=embedding_function
)

def store_memory(query, answer):
    collection.add(
        documents=[answer],
        metadatas=[{"query": query}],
        ids=[query]
    )

def retrieve_memory(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results["documents"]



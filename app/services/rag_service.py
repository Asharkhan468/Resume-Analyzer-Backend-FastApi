from uuid import uuid4

from app.database.chroma import collection
from app.services.embedding_service import get_embedding_model

embedding_model = get_embedding_model()


def store_chunks(chunks):
    documents = []
    ids = []
    embeddings = []

    for chunk in chunks:
        documents.append(chunk.page_content)
        ids.append(str(uuid4()))
        embeddings.append(
            embedding_model.embed_query(
                chunk.page_content
            )
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )


def retrieve_chunks(question):

    question_embedding = embedding_model.embed_query(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    return results["documents"][0]
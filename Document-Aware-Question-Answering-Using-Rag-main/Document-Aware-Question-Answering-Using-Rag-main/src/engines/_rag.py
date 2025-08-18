from __future__ import annotations

from typing import Generator
from uuid import NAMESPACE_DNS, uuid5

import ollama
from chromadb import (
    Client,
    Collection,
    Documents,
    EmbeddingFunction,
    Embeddings,
    PersistentClient,
)
from semantic_text_splitter import TextSplitter

from ._templates import system_message, user_message


class RAGEngine:
    def __init__(
        self,
        embedder: EmbeddingFunction,
        model: str,
        *,
        persist_path: str | None = None,
        collection_name: str = "default",
    ) -> None:
        self.__embedder = embedder
        self.__ollama_model = model
        self.__chroma_client = (
            PersistentClient(path=persist_path) if persist_path else Client()
        )
        self.__collection = self.__chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.__embedder,
            configuration={"hnsw": {"space": "cosine"}},
        )
        self.__text_splitter = TextSplitter(capacity=100, overlap=50)

    @property
    def embedder(self) -> EmbeddingFunction:
        return self.__embedder

    @property
    def chroma_collection(self) -> Collection:
        return self.__collection

    @property
    def text_splitter(self) -> TextSplitter:
        return self.__text_splitter

    @staticmethod
    def __index_chunks(chunk: list[str]) -> dict[str, str]:
        processed_data = {}
        for data in chunk:
            for document in data:
                uid = uuid5(namespace=NAMESPACE_DNS, name=document)
                processed_data[str(uid)] = document
        return processed_data

    def add_data(self, data: str, *, upsert: bool = False) -> None:
        chunks = self.text_splitter.chunk_all([data])
        indexed_chunks = self.__index_chunks(chunks)
        ids = list(indexed_chunks.keys())
        documents = list(indexed_chunks.values())
        if upsert:
            self.chroma_collection.upsert(
                ids=ids,
                documents=documents,
            )
        else:
            self.chroma_collection.add(
                ids=ids,
                documents=documents,
            )

    def clear_collection(self) -> None:
        ids = self.chroma_collection.get()["ids"]
        self.chroma_collection.delete(ids=ids)

    def query_data(
        self,
        query: str,
        *,
        n_results: int = 30,
    ) -> dict:
        return self.chroma_collection.query(
            query_texts=query,
            n_results=n_results,
            include=["documents", "distances", "data", "metadatas"],
        )

    def ask(
        self, query: str, *, max_distance: float = 0.8, stream_output: bool = False
    ) -> Generator[str, None, ollama.ChatResponse]:
        response = self.query_data(query=query)
        documents = response["documents"][0]
        distances = response["distances"][0]
        relevant_documents = [
            documents[i] for i, dist in enumerate(distances) if dist < max_distance
        ]
        system_template = system_message.format(context="\n".join(relevant_documents))
        user_template = user_message.format(query=query)
        response = ollama.chat(
            model=self.__ollama_model,
            messages=[
                {"role": "system", "content": system_template},
                {"role": "user", "content": user_template},
            ],
            stream=stream_output,
        )
        if stream_output:
            for chunk in response:
                yield chunk.message.content


class Embedder(EmbeddingFunction):
    def __init__(self, model: str) -> None:
        self.__model = model

    def __call__(self, input: Documents) -> Embeddings:
        if isinstance(input, str):
            input = [input]
        return ollama.embed(model=self.__model, input=input).embeddings

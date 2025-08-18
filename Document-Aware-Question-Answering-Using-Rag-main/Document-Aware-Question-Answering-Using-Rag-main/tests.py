from src.engines import Embedder, RAGEngine

collection_name = "mycollection"
persist_path = "./.testchroma"
embedding_model = "nomic-embed-text:latest"
language_model = "gemma3:4b"
docs_only = False

data = [
    "Sarah bit into the ripe mango and smiled instantly.",
    "Its juicy sweetness reminded her of summer vacations.",
    "She closed her eyes to savor the rich, golden flavor.",
    "“Nothing beats a mango on a hot day,” she said aloud.",
    "Every bite felt like a reward after a long week.",
    "She even kept a special knife just for slicing them.",
    "Her fridge was never without at least two mangoes.",
    "Friends often joked that she should buy a mango tree.",
    "To Sarah, mangoes weren’t just fruit—they were happiness.",
    "She finished the last slice slowly, already craving another.",
]  # Bigger dataset works better

embedder = Embedder(model=embedding_model)
engine = RAGEngine(
    embedder=embedder, model=language_model, collection_name="rag_engine"
)
engine.add_data(data=data)

response = engine.ask("What is a mango in your own theory", docs_only=docs_only)
if docs_only:
    print(response)
else:
    print(response.message.content)
# print(engine.chroma_collection.get()["ids"])

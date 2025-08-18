# Document-Aware Question Answering using RAG

## Overview
This project is about building a simple **document-aware question answering system** using the concept of **Retrieval-Augmented Generation (RAG)**.  

The idea is straightforward: instead of expecting a model to "know everything", we first fetch the most relevant information from the documents we provide, and then use that context to generate an answer. This makes the system more accurate, reliable, and adaptable to different types of content.

In short, the project shows how we can:
- Load and index documents for searching.
- Retrieve passages that are most relevant to a user’s question.
- Pass those passages into a language model to generate an answer that is backed by the document, not just guesswork.
- Create a workflow where search and generation work hand-in-hand.

The end goal is to have a system that can answer questions **based on the documents you supply**, which is useful for tasks like reading PDFs, knowledge base Q&A, or working with company-specific information.

---

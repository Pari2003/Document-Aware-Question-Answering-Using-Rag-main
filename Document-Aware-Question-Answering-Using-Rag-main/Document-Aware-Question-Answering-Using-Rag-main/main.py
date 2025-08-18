from src.webpage import WebUI

webui = WebUI(
    embedding_model="nomic-embed-text:latest",
    language_model="llama3.1:8b-instruct-q6_K",
)
webui.run()

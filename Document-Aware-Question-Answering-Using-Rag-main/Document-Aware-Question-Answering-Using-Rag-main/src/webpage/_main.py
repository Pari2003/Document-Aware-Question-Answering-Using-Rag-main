import streamlit as st
import torch
from unstructured.partition.auto import partition

from src.engines import Embedder, RAGEngine

torch.classes.__path__ = []  # suppress error regarding streamlit deleting torch classes too quickly


class WebUI:
    def __init__(self, *, embedding_model: str, language_model: str) -> None:
        self.__embedding_model = embedding_model
        self.__language_model = language_model

    @staticmethod
    def upload_page() -> None:
        st.html(
            "<h1 style='font-size:300%;text-align:center;'>📑 Advanced Document Analyzer</h1>"
        )
        st.caption(
            "<p style='font-size:105%;text-align:center;'>Upload any document, and use our AI Model to talk with your document!</p>",
            unsafe_allow_html=True,
        )
        st.divider()
        container = st.empty()
        document = container.file_uploader(
            label=" ", accept_multiple_files=False, label_visibility="collapsed"
        )
        if document:
            container.success("Document uploaded!", icon=":material/check_circle:")
            with st.spinner(text="Processing document...", show_time=True):
                elements = partition(file=document)
                data = "\n".join([x.text or "" for x in elements])
                if not data:
                    st.session_state.process_failed = True
                    st.rerun()
                else:
                    st.session_state.engine.add_data(data=data)
                    st.session_state.document = document
                    st.rerun()

    def process_failure_page(self) -> None:
        st.html(
            "<h1 style='font-size:300%;text-align:center;'>⚠︎ Processing Failed</h1>"
        )
        st.caption(
            "<p style='font-size:105%;text-align:center;'>It appears the document you have provided lacks any information in text format.</p>",
            unsafe_allow_html=True,
        )
        st.divider()
        st.text(" ")
        _, col, _ = st.columns([1, 1, 1], gap="small", vertical_alignment="bottom")
        if col.button("Upload another document?", key="emfpage-return"):
            st.session_state.process_failed = False
            st.rerun()

    def conversation_page(self) -> None:
        st.html("<h1 style='font-size:300%;text-align:center;'>💭 Ask me anything</h1>")
        query = st.chat_input(
            placeholder="Chat with your document...",
            key="processpage-chatinput",
        )
        if query:
            with st.chat_message(name="human"):
                st.write(query)
            with st.chat_message(name="ai"):
                with st.spinner(text="Thinking...", show_time=True):
                    response = st.session_state.engine.ask(query, stream_output=True)
                    st.write_stream(response)
        _, col, _ = st.columns([1, 1, 1], gap="small", vertical_alignment="bottom")
        if col.button("Upload another document?", key="convopage-anotherdoc"):
            st.session_state.engine.clear_collection()
            st.session_state.document = None
            st.rerun()

    def state_setup(self) -> None:
        if "loaded" not in st.session_state:
            st.session_state["loaded"] = True
            st.session_state["document"] = None
            st.session_state["engine"] = RAGEngine(
                embedder=Embedder(model=self.__embedding_model),
                model=self.__language_model,
            )
            st.session_state["process_failed"] = False

    def run(self) -> None:
        self.state_setup()
        if st.session_state.process_failed:
            self.process_failure_page()
        else:
            if not st.session_state.document:
                self.upload_page()
            else:
                self.conversation_page()

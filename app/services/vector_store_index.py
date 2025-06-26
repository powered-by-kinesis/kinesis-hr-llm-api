from llama_index.core import VectorStoreIndex, Document
from fastapi import UploadFile
from llama_index.readers.smart_pdf_loader import SmartPDFLoader
from app.core import get_settings
from llmsherpa.readers import LayoutPDFReader

class VectorStoreIndexService:
    def __init__(self, vector_store_index: VectorStoreIndex):
        self.index = vector_store_index
        settings = get_settings()  
        self.pdf_loader = SmartPDFLoader(llmsherpa_api_url=settings.LLM_SHERPA_URL + "&applyOcr=yes")
        self.reader = LayoutPDFReader(settings.LLM_SHERPA_URL)

    def add(self, files: list[UploadFile], metadata: dict | None = None):
        for file in files:
            read_file = file.file.read()
            doc = self.reader.read_pdf(contents=read_file, path_or_url="")
            for chunk in doc.chunks():
                self.index.insert(Document(text=chunk.to_context_text(), extra_info={}))
from llama_index.core import VectorStoreIndex, Document
from fastapi import UploadFile
from llama_index.readers.smart_pdf_loader import SmartPDFLoader
from app.core import get_settings
from llmsherpa.readers import LayoutPDFReader
from typing import Union

class VectorStoreIndexService:
    def __init__(self, vector_store_index: VectorStoreIndex):
        self.index = vector_store_index
        settings = get_settings()  
        self.pdf_loader = SmartPDFLoader(llmsherpa_api_url=settings.LLM_SHERPA_URL + "&applyOcr=yes")
        self.reader = LayoutPDFReader(settings.LLM_SHERPA_URL)

    async def add(self, files: list[Union[UploadFile, str]], metadata: dict | None = None):
        try:
            for file in files:
                if isinstance(file, str):
                    doc = self.reader.read_pdf(path_or_url=file)
                    
                    for chunk in doc.chunks():
                        self.index.insert(Document(text=chunk.to_context_text(), extra_info=metadata))
                else:
                    read_file = file.file.read()
                    doc = self.reader.read_pdf(contents=read_file, path_or_url='')
                    full_text = doc.to_text()
                    print(full_text)
                    for chunk in doc.chunks():
                        self.index.insert(Document(text=chunk.to_context_text(), extra_info=metadata))
        except Exception as e:
            print(f"Error while adding files to vector store index: {e}")
            raise e
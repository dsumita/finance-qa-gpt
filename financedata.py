import requests
import tqdm
from typing import List
from langchain.document_loaders import PyPDFLoader



class PDFReportLOader:
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.pages = []

    def download_pdf(self, url: str) -> str:
            
        try:
            r = requests.get(url)
            r.raise_for_status()
            filename = url.split("/")[-1]
            with open(filename, 'wb') as f:
                f.write(r.content)
            return filename
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")
            return None
            
    def extract_pages(self, filepath: str) -> List[str]:
        try:
            loader = PyPDFLoader(filepath)
            pages = loader.load_and_split()
            return pages
        except Exception as e:
            print(f"Failed to process PDF {filepath}: {e}")
            return []
        
    def load_reports(self) -> List[str]:
        for url in tqdm.tqdm(self.urls):
            filepath = self.download_pdf(url)
            if not filepath:
                continue
            pages = self.extract_pages(filepath)
            self.pages.extend(pages)

        return self.pages
        
    


from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

import os
from dotenv import load_dotenv


class EmbeddingFinData:
    def __init__(self, chunk_size=1000, chunk_overlap=0, dataset_name="financial_data"):
        ''' Intialize the embediing with text splitter and deeplake set up'''
        load_dotenv()

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.dataset_name = dataset_name

        self.text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        self.embeddings = OpenAIEmbeddings()

        self.activeloop_org_id = os.getenv("ACTIVELOOP_ORG_ID")
        self.activeloop_token = os.getenv("ACTIVELOOP_API_KEY")
        self.openai_api_key= os.getenv("OPENAI_API_KEY")
        self.dataset_path = f"hub://{self.activeloop_org_id}/{self.dataset_name}"

        self.db = DeepLake(
            dataset_path=self.dataset_path,
            embedding=self.embeddings,
            token=self.activeloop_token
        )

        self.qa_chain = None

    def process_n_store(self, documents):
        texts = self.text_splitter.split_documents(documents)
        print("Storing embeddings to deeplake...")
        self.db.add_documents(texts)

    def retrive_data(self, model_name = "gpt-3.5-turbo"):
        llm = ChatOpenAI(model=model_name, api_key=self.openai_api_key)
        retriever = self.db.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    def ask_question(self, question: str) -> str:
        print(f"Your Question: {question}")
        answer = self.qa_chain.invoke(question)
        print(f"Answer: {answer}")
        return answer



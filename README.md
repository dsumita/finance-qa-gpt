This repository contains a Python-based Question-Answering system designed to ingest, process, and answer questions about financial reports in PDF format. It leverages LangChain, OpenAI's GPT models, and the DeepLake vector store to create a powerful Retrieval-Augmented Generation (RAG) pipeline.

The system downloads specified financial reports, extracts their text, creates vector embeddings, and stores them in DeepLake. You can then ask questions in natural language, and the system will retrieve relevant information from the documents to generate a precise answer.

How It Works
The workflow is as follows:

1.Data Ingestion: A list of URLs pointing to PDF financial reports is provided. The PDFReportLOader class downloads each PDF.
2.Text Extraction: The text from each page of the downloaded PDFs is extracted using PyPDFLoader.
3.Text Chunking: The extracted text is split into smaller, manageable chunks using CharacterTextSplitter.
4.Embedding & Storage: Each text chunk is converted into a vector embedding using OpenAIEmbeddings. These embeddings are then stored in a persistent DeepLake vector database. This step only needs to be performed once for a given set of documents.
5.Retrieval & Question-Answering: When a user asks a question, a RetrievalQA chain is used. It first retrieves the most relevant text chunks from the DeepLake vector store based on the semantic similarity of the question.
6.Answer Generation: The retrieved text chunks (context) and the original question are passed to a ChatOpenAI model (e.g., gpt-3.5-turbo), which generates a final, context-aware answer.


Setup and Installation
1. Clone the Repository
git clone https://github.com/dsumita/finance-qa-gpt.git
cd finance-qa-gpt
2. Install Dependencies
This project requires several Python packages. You can install them using pip:

pip install langchain langchain-openai deeplake python-dotenv requests tqdm pypdf
3. Set Up Environment Variables
You will need API keys from OpenAI and Activeloop. Create a .env file in the root directory of the project and add your credentials:

OPENAI_API_KEY="sk-..."
ACTIVELOOP_API_KEY="ey..."
ACTIVELOOP_ORG_ID="your-activeloop-org-id"

Code Structure
main.py: The main script that orchestrates the data loading, embedding, and question-answering process. Contains the list of target PDF URLs.
financedata.py: Defines the PDFReportLOader class, responsible for downloading PDFs from URLs and extracting text content using LangChain's PyPDFLoader.
my_text_embedding.py: Contains the EmbeddingFinData class, which handles the core RAG pipeline logic, including text splitting, embedding creation, storage in DeepLake, and setting up the RetrievalQA chain.

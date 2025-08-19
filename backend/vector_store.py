from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

file_path = "indian_food.csv"

loader = CSVLoader(file_path=file_path)
data = loader.load()

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db"  # Where to save data locally, remove if not necessary
)

chunks = text_splitter.split_documents(data)
vector_store.add_documents(chunks)

query = input("Enter Your Query : ")
docs = db.similarity_search(query)


print(docs[0].page_content)
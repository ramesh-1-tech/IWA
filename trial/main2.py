import pandas as pd
import os
import matplotlib.pyplot as plt
from langchain.chains import create_retrieval_chain
from langchain import  hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.retrievers import MultiQueryRetriever
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader

# import getpass

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Data ingestion
loader = CSVLoader("../data/admin_data.csv")
documents = loader.load()

# Initialize the OpenAI LLM
llm = OpenAI(api_key=OPENAI_API_KEY)

# Split (transform)
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
db = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""
You are an assistant for question-answering tasks.You have access to a dataset stored in a CSV file which is in your context. user will ask you questions about the data and you will perform analysis based on that request. Here are some examples of what you can do:

* Calculate summary statistics like average, sum, maximum, and minimum values for a specific column. (e.g., What is the average price?)
* Count the number of entries in the data or for a specific column. (e.g., How many customers are there?)
* You can also request the entire dataframe for further exploration. (e.g., Show me the complete data)


<context>
{context}
</context>
Question: {input}""")

## Create Stuff Docment Chain
document_chain = create_stuff_documents_chain(llm, prompt)

# Create a retriever
"""
Retrievers: A retriever is an interface that returns documents given
 an unstructured query. It is more general than a vector store.
 A retriever does not need to be able to store documents, only to 
 return (or retrieve) them. Vector stores can be used as the backbone
 of a retriever, but there are other types of retrievers as well. 
 https://python.langchain.com/docs/modules/data_connection/retrievers/   
"""
# retriever = db.as_retriever(search_kwargs={'k': 100})
retriever = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(), llm=llm
)

"""
Retrieval chain:This chain takes in a user inquiry, which is then
passed to the retriever to fetch relevant documents. Those documents 
(and original inputs) are then passed to an LLM to generate a response
https://python.langchain.com/docs/modules/chains/
"""
system_prompt = hub.pull('rlm/rag-prompt')
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "Create a chart of top 5 patient based on billing amount"})

# query = "Total of all billing amount"
# docs = db.similarity_search(query)
#
# chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
#

breakpoint()

# os.environ["OPENAI_API_KEY"] = getpass.getpass()
#
# # Load CSV data
# df = pd.read_csv('data/admin_data.csv')
# print("CSV file read done")
# # Initialize the OpenAI embedding model
# embedding_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
#
# # Create embeddings for the data
# print("OpenAI model loaded")
# embeddings = embedding_model.embed_documents(df)
# # embeddings = df.apply(lambda row: embedding_model.embed_documents(row.astype(str).tolist()), axis=1)
#
# # Convert embeddings to a list of vectors
# print("OpenAI embedding model vector")
# breakpoint()
#
#
# # Create the retrieval and QA chain
# #
# # retrieval_qa = RetrievalQA(
# #     vectorstore=faiss_index,
# #     llm=llm,
# #     retriever_args={"top_k": 5}  # Adjust top_k based on your needs
# # )
#
# # Define a function to generate responses
# def generate_response(prompt):
#     return retrieval_qa.run(prompt)
#
# # Function to generate charts from data
# def generate_chart(data, chart_type='bar'):
#     if chart_type == 'bar':
#         data.plot(kind='bar')
#     elif chart_type == 'line':
#         data.plot(kind='line')
#     elif chart_type == 'scatter':
#         data.plot(kind='scatter', x=data.columns[0], y=data.columns[1])
#     # Add more chart types as needed
#
#     plt.show()
#
# # Example usage
# prompt = "Show me the sales data for the last quarter"
# response = generate_response(prompt)
#
# # Check if a chart is requested in the response
# if 'chart' in response.lower():
#     chart_data = df[df['your_filter_column'] == 'filter_value']  # Filter data based on prompt
#     generate_chart(chart_data, chart_type='bar')
# else:
#     print(response)

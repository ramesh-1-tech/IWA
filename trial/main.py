from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
loader = CSVLoader(file_path="../data/admin_data.csv")
docs = loader.load()
chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)

# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Embed
vectorstore = Chroma.from_documents(documents=splits,
                                    embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()


#### RETRIEVAL and GENERATION ####

# Prompt
prompt = hub.pull("rlm/rag-prompt")

# LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Chain
rag_chain = (
    {"context": retriever , "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
rag_chain2 = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)


# retriever_res_data = retriever.invoke("Can LangSmith help test my LLM applications?")
#
# SYSTEM_TEMPLATE = """
# Answer the user's questions based on the below context.
# If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":
#
# <context>
# {context}
# </context>
# """
#
# question_answering_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             SYSTEM_TEMPLATE,
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )
#
# document_chain = create_stuff_documents_chain(chat, question_answering_prompt)
# doc_chain_res = document_chain.invoke(
#     {
#         "context": retriever_res_data,
#         "messages": [
#             HumanMessage(content="Create a chart of top 5 billing amount and age")
#         ],
#     }
# )
#
#


breakpoint()

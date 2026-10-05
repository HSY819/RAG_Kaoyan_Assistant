
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

print("--- 1. 正在加载PDF ---")
loader = PyPDFLoader("./test.pdf")
docs = loader.load()
print(f"加载成功，共 {len(docs)} 页")
print(f"第一页内容预览：[{docs[0].page_content[:100]}]")

print("--- 2. 正在切分文本 ---")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
print(f"切分完成，共 {len(splits)} 个文本块")

print("--- 3. 正在向量化并存入ChromaDB（首次运行可能需下载模型，稍等）---")
embeddings = DashScopeEmbeddings(model="text-embedding-v2")
# 向量数据会保存在当前目录的 chroma_db 文件夹中
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")
print("向量化存储完成！")

print("--- 4. 组装RAG链路 ---")
llm = ChatTongyi(model="qwen-plus")
prompt = ChatPromptTemplate.from_template("""
你是考研辅导助手。请严格根据以下上下文回答问题。
如果上下文中没有答案，请直接说“资料中未提及”，不要自己编造。
请在回答末尾标注参考的来源页码。

<上下文>
{context}
</上下文>

用户提问：{input}
""")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # 检索最相似的3块
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

print("\n--- 5. 开始测试 ---")
# 根据你的PDF内容，换一个问题。比如你的PDF是关于数据结构，就问数据结构的问题。
response = rag_chain.invoke({"input": "408考试的试卷满分是多少？考试时间是多少？"})
print("\n回答：", response["answer"])

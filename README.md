# 基于RAG的计算机考研辅助学习系统（最小Demo）

## 💡 项目背景
通用大模型在计算机考研的专业课问答中极易产生“幻觉”，且考研资料分散、缺乏溯源。本项目基于RAG（检索增强生成）技术，构建了一个最小可行系统，旨在基于官方考研大纲，实现**精准、可溯源**的智能问答，解决大模型胡说八道的问题。

## 🛠️ 技术栈
- **核心框架**：LangChain
- **大模型（LLM）**：阿里云百炼 (Qwen-plus)
- **向量模型（Embedding）**：DashScopeEmbeddings (text-embedding-v2)
- **向量数据库**：ChromaDB
- **文档解析**：PyPDFLoader
- **开发环境**：Python 3.13 + PyCharm

## 🔄 核心流程
1. **文档加载**：读取本地考研大纲PDF（支持17页大纲文本）。
2. **文本切分**：使用 `RecursiveCharacterTextSplitter` 对文档进行切分（chunk_size=500, overlap=50）。
3. **向量化与存储**：将切分后的文本块通过百炼Embedding模型向量化，持久化存入ChromaDB。
4. **RAG检索问答**：基于用户提问检索最相关的3个文本块，拼接Prompt后交给大模型生成回答。
5. **防幻觉机制**：通过精心设计的Prompt，强制要求大模型**必须基于上下文回答**，并在末尾标注参考页码。如果上下文中没有答案，则主动拒绝回答。

## 📸 运行效果
<img width="2724" height="1394" alt="image" src="https://github.com/user-attachments/assets/fef06639-5ffb-4f00-b337-c9198a1c3124" />
<img width="2652" height="748" alt="image" src="https://github.com/user-attachments/assets/615883a3-76c6-4ee4-a23c-df8928fd07db" />


*（终端输出示例）*
```text
--- 1. 正在加载PDF ---
加载成功，共 17 页
第一页内容预览：[2026
考研
408
考试大纲
科目
25
大纲
26
大纲
计算机网络
3.ISO/OSI
参考模型和
TCP/IP
模型
3.ISO/OSI
参考模型和
TCP/IP
参考
模
型
【
26
改]
--- 2. 正在切分文本 ---
切分完成，共 19 个文本块
--- 3. 正在向量化并存入ChromaDB（首次运行可能需下载模型，稍等）---
向量化存储完成！
--- 4. 组装RAG链路 ---

--- 5. 开始测试 ---

回答： 408考试的试卷满分为150分，考试时间为180分钟。  
参考的来源页码：Ⅲ试卷满分及试卷结构 第1条

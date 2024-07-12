'''TO LOAD A TEXT FILE'''

from langchain_community.document_loaders import TextLoader
loader=TextLoader('speech.txt')
print(loader.load())

'''TO LOAD A PDF'''
from langchain_community.document_loaders import PyPDFLoader
loader1=PyPDFLoader('attention.pdf')
print(loader1.load())

'''WEB BASED LOADER'''
from langchain_community.document_loaders import WebBaseLoader
import bs4
loader=WebBaseLoader(web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
                     bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                         class_=("post-title","post-content","post-header")
                     ))
                     )

'''WikiPedia Loader'''
from langchain_community.document_loaders import WikipediaLoader
docs = WikipediaLoader(query="Generative AI", load_max_docs=2).load()
len(docs)
print(docs)
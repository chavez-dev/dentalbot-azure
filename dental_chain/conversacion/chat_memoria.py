from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dental_chain.llm import llm
from dental_chain.utils.constants import SYSTEM

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("placeholder", "{chat_conversation}")
])

chat_chain = prompt | llm | StrOutputParser()

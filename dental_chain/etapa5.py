from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dental_chain.llm import llm

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "Eres un asistente de DentalCare Tacna. "
     "Respondes de forma cordial y clara. "
     "Recuerda lo que el usuario ha dicho antes y da continuidad a la conversación."),
    ("placeholder", "{chat_conversation}")
])

chat_chain = prompt | llm | StrOutputParser()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dental_chain.llm import llm

SYSTEM = (
    "Eres un asistente de DentalCare Tacna. "
    "Respondes de forma cordial y clara. "
    "Recuerda lo que el usuario ha dicho antes y da continuidad a la conversación. "
    "Si el usuario se presenta, recuerda su nombre durante la sesión actual. "
    "Responde con naturalidad y evita repetir preguntas innecesarias."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("placeholder", "{chat_conversation}")
])

chat_chain = prompt | llm | StrOutputParser()

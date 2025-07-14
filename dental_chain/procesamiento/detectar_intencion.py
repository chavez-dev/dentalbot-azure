from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dental_chain.llm import llm

ejemplos = [
    {"mensaje": "Hola, quiero agendar una cita para ortodoncia el martes",
        "intencion": "reserva"},
    {"mensaje": "¿Qué horarios tienen disponibles?", "intencion": "pregunta"},
    {"mensaje": "Muchas gracias por la atención", "intencion": "chat"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{mensaje}"),
    ("ai", "{intencion}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=ejemplos,
    example_prompt=example_prompt,
)

intencion_prompt = ChatPromptTemplate.from_messages([
    few_shot_prompt,
    ("system",
     "Eres un sistema que clasifica la intención de un mensaje en DentalCare Tacna. "
     "Las posibles intenciones son: reserva, pregunta, chat. "
     "RESPONDE SOLO con una palabra: reserva, pregunta o chat."),
    ("human", "{mensaje}")
])

intencion_chain = intencion_prompt | llm | StrOutputParser()

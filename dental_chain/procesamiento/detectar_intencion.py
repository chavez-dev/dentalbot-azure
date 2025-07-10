from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dental_chain.llm import llm

intencion_prompt = ChatPromptTemplate.from_template("""
Eres un sistema que clasifica la intención de un mensaje enviado por un usuario en una clínica dental.

Las posibles intenciones son:
- "reserva": si el mensaje contiene datos o intención clara de reservar cita (nombre, fecha, yape, etc.)
- "pregunta": si el mensaje contiene preguntas informativas sobre servicios, horarios, precios, etc.
- "chat": si el mensaje es simplemente saludo, agradecimiento, o conversación sin objetivo claro.

Solo responde con una palabra: reserva, pregunta o chat.

Mensaje:
{mensaje}
""")

intencion_chain = intencion_prompt | llm | StrOutputParser()

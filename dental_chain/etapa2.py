from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from dental_chain.llm import llm

class QA(BaseModel):
    pregunta: str
    respuesta: str

parser = JsonOutputParser(pydantic_object=QA)

prompt = ChatPromptTemplate.from_template(
    """
Eres un asistente de DentalCare Tacna.

Tu tarea es responder la siguiente pregunta de manera breve (máx. 3 frases) y **devolver la salida en JSON válido** con los siguientes campos:
- pregunta: la pregunta original
- respuesta: la respuesta generada

{format_instructions}

Pregunta:
{pregunta}
"""
).partial(format_instructions=parser.get_format_instructions())

respuesta_chain = prompt | llm | parser

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from dental_chain.llm import llm

class RespuestaSimple(BaseModel):
    respuesta: str

parser = JsonOutputParser(pydantic_object=RespuestaSimple)

prompt = ChatPromptTemplate.from_template(
    """
Eres un asistente profesional de DentalCare Tacna.

Responde este mensaje en máximo 2 frases, de forma clara y amigable. Devuelve un JSON válido con este campo:

- respuesta: tu mensaje.

{format_instructions}

Mensaje:
{mensaje}
"""
).partial(format_instructions=parser.get_format_instructions())

simple_chain = prompt | llm | parser

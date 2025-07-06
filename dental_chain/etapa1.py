from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from typing import List
from dental_chain.llm import llm

class Pregunta(BaseModel):
    texto: str

prompt = PromptTemplate(
    input_variables=["mensaje"],
    template="""
Extrae cada pregunta individual del siguiente mensaje del usuario:

"{mensaje}"

Devuelve una lista JSON como esta:
[
  {{ "texto": "¿Cuál es el horario?" }},
  {{ "texto": "¿Puedo agendar una cita?" }}
]
"""
)

parser = JsonOutputParser(pydantic_object=List[Pregunta])
tagging_chain = prompt | llm | parser

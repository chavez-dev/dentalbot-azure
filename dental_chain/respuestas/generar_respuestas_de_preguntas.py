from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from dental_chain.llm import llm
from dental_chain.utils.constants import SERVICIOS_LISTA, SYSTEM


class QA(BaseModel):
    pregunta: str
    respuesta: str


parser = JsonOutputParser(pydantic_object=QA)

prompt = ChatPromptTemplate.from_template(
    """
Eres un bot de una Clinica Dental, ten en consideracion lo siguiente:
{system}
Tu tarea es responder la siguiente pregunta de manera breve (máx. 3 frases) y **devolver la salida en JSON válido** con los siguientes campos:
- pregunta: la pregunta original
- respuesta: la respuesta generada

{format_instructions}

Pregunta:
{pregunta}
"""
)

respuesta_chain = (
    prompt.partial(system=SERVICIOS_LISTA,format_instructions=parser.get_format_instructions())
    | llm
    | parser
)

formatear_entrada = RunnableLambda(
    lambda preguntas: {
        str(i): {"pregunta": p["texto"]} for i, p in enumerate(preguntas)
    }
)


def wrap_value(v):
    return RunnableLambda(lambda _: v)


crear_parallel_chain = formatear_entrada | RunnableLambda(
    lambda inputs: RunnableParallel({
        key: wrap_value(value) | respuesta_chain
        for key, value in inputs.items()
    })
)

formatear_salida = RunnableLambda(lambda d: list(d.values()))

procesar_preguntas_chain = crear_parallel_chain | formatear_salida

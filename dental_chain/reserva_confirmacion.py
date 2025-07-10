import requests
import uuid
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from dental_chain.llm import llm

GOOGLE_FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdOhSV_sV2aQMpf_ITg8VXxMmw6ENm5Xbi_cLF9EzfDVcsbRg/formResponse"

FORM_FIELDS = {
    "id": "entry.947239356",
    "nombre": "entry.309627727",
    "dni": "entry.1124227301",
    "telefono": "entry.105580532",
    "servicio": "entry.2113367294",
    "fecha_programada": "entry.1664945397",
    "tracking": "entry.758801494"
}

class Reserva(BaseModel):
    nombre: str = Field(description="Nombre completo del paciente")
    dni: str = Field(description="Número de DNI del paciente")
    telefono: str = Field(description="Número de teléfono del paciente")
    servicio: str = Field(description="Servicio dental solicitado")
    fecha_programada: str = Field(
        description="Fecha y hora de la cita solicitada")
    tracking: str = Field(
        description="Código de verificación o seguimiento de Yape")


def enviar_a_google_forms(reserva_dict):
    reserva = Reserva(**reserva_dict) 
    reserva_id = str(uuid.uuid4())
    payload = {
        FORM_FIELDS["id"]: reserva_id,
        FORM_FIELDS["nombre"]: reserva.nombre,
        FORM_FIELDS["dni"]: reserva.dni,
        FORM_FIELDS["telefono"]: reserva.telefono,
        FORM_FIELDS["servicio"]: reserva.servicio,
        FORM_FIELDS["fecha_programada"]: reserva.fecha_programada,
        FORM_FIELDS["tracking"]: reserva.tracking,
    }
    try:
        response = requests.post(
            GOOGLE_FORMS_URL,
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded", "mode": "no-cors"}
        )
        print("📤 Datos enviados a Google Forms")
        print(f"🆔 ID generado: {reserva_id}")
        return f"✅ Reserva registrada correctamente. Código: {reserva_id}"
    except Exception as e:
        print("❌ Error al enviar a Google Forms:", e)
        return "❌ No se pudo registrar la reserva"


parser = JsonOutputParser(pydantic_object=Reserva)

prompt = ChatPromptTemplate.from_template("""
Eres un asistente de DentalCare Tacna. Un usuario ha proporcionado información para reservar una cita dental. 
Extrae los siguientes datos en formato JSON estrictamente válido:

- nombre
- dni
- telefono
- servicio
- fecha_programada
- tracking

{format_instructions}

Mensaje:
{mensaje}
""")

extract_chain = prompt.partial(
    format_instructions=parser.get_format_instructions()) | llm | parser

reserva_chain = extract_chain | RunnableLambda(enviar_a_google_forms)

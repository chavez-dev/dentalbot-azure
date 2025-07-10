import requests
import uuid
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableMap
from pydantic import BaseModel, Field
from dental_chain.llm import llm
from dental_chain.utils.constants import FORM_FIELDS, GOOGLE_FORMS_URL, SERVICIOS_LISTA


class Reserva(BaseModel):
    nombre: str = Field(description="Nombre completo del paciente")
    dni: str = Field(description="Número de DNI del paciente")
    celular: str = Field(description="Número de teléfono del paciente")
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
        FORM_FIELDS["celular"]: reserva.celular,
        FORM_FIELDS["servicio"]: reserva.servicio.upper(),
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


def decision_logic(output):
    datos = output["datos"]
    valido_datos = output["valido_datos"]
    valido_servicio = output["valido_servicio"]

    if valido_datos["valido"] and valido_servicio:
        confirmacion = confirmacion_chain.invoke(datos)
        resultado_envio = enviar_a_google_forms(datos)
        return f"{confirmacion}\n\n{resultado_envio}"

    if not valido_datos["valido"]:
        faltantes = valido_datos["faltantes"]
        mensaje = "⚠️ No puedo realizar una reserva porque faltan los siguientes datos: " + \
            ", ".join(faltantes)
        return mensaje

    servicio = datos.get("servicio", "").strip()
    return f"🚫 El servicio '{servicio}' no está disponible en DentalCare Tacna. Revisa la lista de servicios ofrecidos."


def validar_servicio(reserva: dict) -> bool:
    servicio = reserva.get("servicio", "").strip().lower()
    return servicio in [s.lower() for s in SERVICIOS_LISTA]


def validar_datos(reserva: dict) -> dict:
    campos_requeridos = ["nombre", "dni", "celular",
                         "servicio", "fecha_programada", "tracking"]
    campos_faltantes = [
        campo for campo in campos_requeridos if not reserva.get(campo)]
    return {
        "valido": len(campos_faltantes) == 0,
        "faltantes": campos_faltantes
    }


def mensaje_error_si_incompleto(valido: bool) -> str:
    if valido:
        return "✅ Datos completos. Procediendo con la reserva..."
    return "⚠️ Faltan datos importantes. Asegúrate de proporcionar nombre, DNI, teléfono, servicio, fecha y código de Yape."


parser = JsonOutputParser(pydantic_object=Reserva)
prompt = ChatPromptTemplate.from_template("""
Eres un asistente de DentalCare Tacna. Un usuario ha proporcionado información para reservar una cita dental. 
Extrae los siguientes datos en formato JSON estrictamente válido:

- nombre
- dni
- celular
- servicio
- fecha_programada
- tracking

{format_instructions}

Mensaje:
{mensaje}
""")

confirmacion_prompt = ChatPromptTemplate.from_template("""
Devuelve solo el siguiente texto:
📅 ¡Reserva Confirmada!

🙋‍♂️ Paciente: {nombre}  
🦷 Servicio: {servicio}  
🗓️ Fecha programada: {fecha_programada}

📍 Te esperamos en DentalCare Tacna.
🕒 Por favor llega 10 minutos antes de tu cita.

Gracias por confiar en nosotros 💙
""")

confirmacion_chain = confirmacion_prompt | llm | StrOutputParser()

validar_datos_chain = RunnableLambda(validar_datos)
validar_servicio_chain = RunnableLambda(validar_servicio)

extract_chain = prompt.partial(
    format_instructions=parser.get_format_instructions()) | llm | parser
validacion_chain = RunnableMap({
    "datos": lambda r: r,
    "valido_datos": validar_datos_chain,
    "valido_servicio": validar_servicio_chain
})
decision_chain = RunnableLambda(decision_logic)

reserva_chain = extract_chain | validacion_chain | decision_chain

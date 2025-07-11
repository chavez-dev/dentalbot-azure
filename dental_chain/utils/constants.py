SERVICIOS_LISTA = [
    "Ortodoncia",
    "Limpieza dental",
    "Blanqueamiento",
    "Extracción"
]

SERVICIOS_STR = ", ".join(SERVICIOS_LISTA)

SYSTEM = (
    f"Eres un asistente de DentalCare Tacna. "
    f"Respondes de forma cordial y clara. "
    f"Recuerda lo que el usuario ha dicho antes y da continuidad a la conversación. "
    f"Si el usuario se presenta, recuerda su nombre durante la sesión actual. "
    f"Responde con naturalidad y evita repetir preguntas innecesarias. "
    f"Los servicios disponibles son: {SERVICIOS_STR}."
)


GOOGLE_FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdOhSV_sV2aQMpf_ITg8VXxMmw6ENm5Xbi_cLF9EzfDVcsbRg/formResponse"

FORM_FIELDS = {
    "id": "entry.516806082",
    "nombre": "entry.309627727",
    "dni": "entry.1124227301",
    "celular": "entry.105580532",
    "servicio": "entry.2113367294",
    "fecha_programada": "entry.1664945397",
    "tracking": "entry.758801494"
}

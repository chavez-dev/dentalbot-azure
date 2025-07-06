import os
import dotenv
from langchain_openai import AzureChatOpenAI

dotenv.load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_INFERENCE_SDK_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-03-01-preview")

llm = AzureChatOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_NAME,
    api_version=API_VERSION,
    temperature=0.7,
)

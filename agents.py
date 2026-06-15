import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from state import LegalAuditState


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

def type_identifier(state: LegalAuditState):
    prompt = f"""You are an expert Indian legal document analyst.
    
    Identify the type of this legal document.
    Common Indian legal document types: rent_agreement, rti_application, vendor_contract, consumer_complaint.
    Return only the document type in snake_case, nothing else. If unsure return unknown.

    Document:
    {state['raw_document']}"""

    result = model.invoke(prompt)
    return {"document_type": result.content.strip().lower()}

def meaning_extractor(state : LegalAuditState):
    prompt = f"""You are an expert Indian legal document analyst.

        I will give you a raw legal document and its type. Your task is to extract all important information from the document.

        Rules:
        - Return ONLY a valid JSON object, nothing else
        - No explanation, no markdown, no backticks, no additional text
        - Just raw JSON starting with {{ and ending with }}
        - Extract all parties, dates, amounts, addresses, and key terms
        - Keep values concise, not full sentences

        Document Type: {state['document_type']}

        Document:
        {state['raw_document']}

        Return only JSON:"""

    result = model.invoke(prompt)
    cleaned = result.content.strip()
    cleaned = cleaned.strip()
    parsed = json.loads(cleaned)
    return {"extracted_clauses": parsed}
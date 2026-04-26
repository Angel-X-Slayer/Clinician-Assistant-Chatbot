from typing import List, Dict
from pydantic import BaseModel


class ClinicalSchema(BaseModel):
    chief_complaint: str = ""
    symptoms: List[str] = []
    duration: str = ""
    severity: str = ""
    associated_symptoms: List[str] = []
    negatives: List[str] = []
    past_medical_history: str = ""
    surgeries: List[str] = []
    hospitalizations: List[str] = []


class GraphState(BaseModel):
    messages: List[Dict[str, str]] = []
    clinical_data: ClinicalSchema = ClinicalSchema()
    stage: str = "cc"

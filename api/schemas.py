from pydantic import BaseModel


class AskRequest(BaseModel):
    document_id: str
    question: str
    output_language: str = "English"


class SummaryRequest(BaseModel):
    document_id: str
    summary_type: str = "short"
    output_language: str = "English"


class StudyRequest(BaseModel):
    document_id: str
    output_language: str = "English"
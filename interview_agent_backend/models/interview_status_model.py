from typing import List, Optional

from pydantic import BaseModel, Field

class Text(BaseModel):
    text: List[str]

class FulfillmentMessage(BaseModel):
    text: Text

class QueryParameters(BaseModel):
    jobID: List[str]
    user_email: str

class OutputContextParameters(BaseModel):
    no_input: Optional[float] = Field(None, alias="no-input")
    no_match: Optional[float] = Field(None, alias="no-match")
    jobID: Optional[List[str]] = None
    jobID_original: Optional[List[str]] = Field(None, alias="jobID.original")
    user_email: Optional[str] = None
    user_email_original: Optional[str] = Field(None, alias="user_email.original")

class OutputContext(BaseModel):
    name: str
    lifespanCount: Optional[int] = None
    parameters: OutputContextParameters

class Intent(BaseModel):
    name: str
    displayName: str

class QueryResult(BaseModel):
    queryText: str
    action: str
    parameters: QueryParameters
    allRequiredParamsPresent: bool
    fulfillmentMessages: List[FulfillmentMessage]
    outputContexts: List[OutputContext]
    intent: Intent
    intentDetectionConfidence: float
    languageCode: str

class OriginalDetectIntentRequest(BaseModel):
    source: str
    payload: dict

class InterviewStatusRequest(BaseModel):
    responseId: str
    queryResult: QueryResult
    originalDetectIntentRequest: OriginalDetectIntentRequest
    session: str

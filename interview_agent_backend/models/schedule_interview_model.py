from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime


class DateTimeValue(BaseModel):
    date_time: str


class QueryParameters(BaseModel):
    # The date-time is actually a nested object with a date_time field
    date_time: DateTimeValue = Field(..., alias="date-time")


class Text(BaseModel):
    text: List[str]


class FulfillmentMessage(BaseModel):
    text: Text


class OutputContextParameters(BaseModel):
    # Date time in the output contexts also follows the same pattern
    date_time: Optional[DateTimeValue] = Field(None, alias="date-time")
    date_time_original: Optional[str] = Field(None, alias="date-time.original")
    job_id: Optional[List[str]] = Field(None, alias="jobID")
    job_id_original: Optional[List[str]] = Field(None, alias="jobID.original")
    user_email: Optional[str] = Field(None, alias="user_email")
    user_email_original: Optional[str] = Field(None, alias="user_email.original")
    no_input: Optional[int] = Field(None, alias="no-input")
    no_match: Optional[int] = Field(None, alias="no-match")


class OutputContext(BaseModel):
    name: str
    lifespan_count: Optional[int] = Field(None, alias="lifespanCount")
    parameters: OutputContextParameters


class Intent(BaseModel):
    name: str
    display_name: str = Field(..., alias="displayName")


class QueryResult(BaseModel):
    query_text: str = Field(..., alias="queryText")
    parameters: QueryParameters
    all_required_params_present: bool = Field(..., alias="allRequiredParamsPresent")
    fulfillment_messages: List[FulfillmentMessage] = Field(..., alias="fulfillmentMessages")
    output_contexts: List[OutputContext] = Field(..., alias="outputContexts")
    intent: Intent
    intent_detection_confidence: float = Field(..., alias="intentDetectionConfidence")
    language_code: str = Field(..., alias="languageCode")


class OriginalDetectIntentRequest(BaseModel):
    source: str
    payload: Dict[str, Any]


class DialogflowWebhookResponse(BaseModel):
    response_id: str = Field(..., alias="responseId")
    query_result: QueryResult = Field(..., alias="queryResult")
    original_detect_intent_request: OriginalDetectIntentRequest = Field(
        ..., alias="originalDetectIntentRequest"
    )
    session: str

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True
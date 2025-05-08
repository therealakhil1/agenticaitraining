import json
from typing import List, Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI(title="Interview Agent API")

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

class DialogflowRequest(BaseModel):
    responseId: str
    queryResult: QueryResult
    originalDetectIntentRequest: OriginalDetectIntentRequest
    session: str

#TODO: if you want to do more replace this dict with a database or some shit, and extend functionality of actually
# taking interviews.
interview_status_to_user_map = {
    'akhilspalli@gmail.com': {
        '123456': True,
        '456789': False
    },
    'abc.def@outlook.com': {
        '994738': True
    },
    'hello.i.am.not.a.soda.bottle@chips.com': {
        '111111': False
    }
}


def interview_status(request):
    jobid = None
    email = request.queryResult.parameters.user_email
    for job in request.queryResult.parameters.jobID:
        if len(job) == 6:
            jobid = job
            break

    is_qualified_to_interview = interview_status_to_user_map.get(email, {jobid:False}).get(jobid, False)

    fulfillment_text = "Yes you're profile was screened for an interview round" if is_qualified_to_interview else "No you're profile was not screened for an interview round"

    output_context =str(request.queryResult.outputContexts[0].name)

    payload = {
        "fulfillmentText": fulfillment_text
    }
    if is_qualified_to_interview:
        payload["outputContexts"] = [{
            "name": output_context,
            "lifespanCount": 5,
            "parameters": {
                "jobId": jobid,
                "userEmail": email
            }
        }]
    else:
        payload["followupEventInput"] = {
            "name": "end_conversation",
            "languageCode": "en-US"
        }

    print(payload)
    return json.dumps(payload)


def schedule_interview(request):
    print('bye')
    # print(request)

def user_job_offer(request):
    pass


intent_name_to_serve_function_mapping = {
    "Ask about interview": interview_status,
    'Confirm interview dates': schedule_interview,
    'Job offer': user_job_offer
}

@app.post("/webhook")
async def root(request: DialogflowRequest = Body(...)):
    print('hi')
    return intent_name_to_serve_function_mapping.get(request.queryResult.intent.displayName)(request)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
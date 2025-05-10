import json
from http.client import HTTPException
from typing import Union

from fastapi import FastAPI, Body, Request
from models.interview_status_model import InterviewStatusRequest
from models.schedule_interview_model import DialogflowWebhookResponse

app = FastAPI(title="Interview Agent API")

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
    print(request)

def user_job_offer(request):
    pass


# intent_name_to_serve_function_mapping = {
#     "Ask about interview": interview_status,
#     'Confirm interview dates': schedule_interview,
#     'Job offer': user_job_offer
# }

@app.post("/webhook")
async def root(req: Request):
    body = await req.json()
    intent = body["queryResult"]["intent"]["displayName"]
    if intent == "Ask about interview":
        parsed = InterviewStatusRequest.parse_obj(body)
        return interview_status(parsed)
    elif intent == "Confirm interview dates":
        parsed = DialogflowWebhookResponse.parse_obj(body)
        return schedule_interview(parsed)
    else:
        raise HTTPException(400, "Unknown intent")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
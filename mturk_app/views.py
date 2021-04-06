import json
import os
import secrets
import string
from copy import deepcopy

import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from operator import itemgetter

from mturk_app.models import Participant

DEV_ENVIROMENT_BOOLEAN = True

if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"  # Development environment (Sandbox)
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"  # Production

@csrf_exempt
def home(request):

    # The following code segment can be used to check if the turker has accepted the task yet
    if request.GET.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        # Our worker hasn't accepted the HIT (task) yet
        pass
        print("You should accept the task to see the game")
        return HttpResponse("You should accept the task to see the game")
    elif request.GET.get("assignmentId") is not None:
        # Our worker accepted the task
        print("Task accepted")
        pass
    else:
        return HttpResponse("404")

    render_data = {
        "worker_id": request.GET.get("workerId"),
        "assignment_id": request.GET.get("assignmentId"),
        "amazon_host": AMAZON_HOST,
        "hit_id": request.GET.get("hitId"),
        "some_info_to_pass": request.GET.get("someInfoToPass")
    }

    print("render data: ", render_data)

    # based on data, redirect to game type
    return render(request, "mturk_app/template.html", render_data)

# Gets called after the form is submitted. Saves the data into S3 and database.
@csrf_exempt
def post_data(request):
    data = request.POST.get('data', None)
    worker_id = request.POST.get('workerId', None)

    print("Finished, submitting to s3. ID: ", worker_id, " data: ", data)

    from datetime import datetime
    dt = datetime.today().strftime('%Y-%m-%d=%H:%M:%S')

    aws_id = os.environ['AWS_ID']
    aws_secret_key = os.environ['AWS_SECRET_KEY']
    aws_bucket_name = os.environ['BUCKET_NAME']

    AWS_ACCESS_KEY = aws_id
    AWS_SECRET_KEY = aws_secret_key

    final_data = data

    filename = data + "/" + dt + "_" + worker_id + ".json"

    print("writing ", filename)

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        body = json.dumps(final_data).encode()
        s3.put_object(Body=body, Bucket=aws_bucket_name, Key=filename)

    except ClientError as e:
        print("Client error.")
        # with open(filename, 'w') as f:
        #    json.dump(final_data, f)


    context = {
        "data": request.POST.get("data"),
        "assignment_id": request.POST.get("assignmentId"),
        "worker_id": request.POST.get("workerId"),
        "hit_id": request.POST.get("hitId"),
    }

    save_into_db(context)

    return render(request, "mturk_app/finished.html", context)


def save_into_db(context):
    data = context["data"]
    assignment_id = context["assignment_id"]
    worker_id = context["worker_id"]
    hit_id = context["hit_id"]

    participant = Participant(data=data, assignment_id=assignment_id, worker_id=worker_id, hit_id=hit_id)
    participant.save()

    print("Participant ", worker_id, " succesfully saved.")


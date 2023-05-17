import json
import os
import datetime
import uuid

import boto3

from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

# @app.post("/hello")
# def hello_post():
#     return {"message": "hello post!"}
# post_data: dict = app.current_event.json_body
@app.post("/hello")
def simple_post():
    post_data: dict = app.current_event.json_body
    return {"create": post_data["id"]}
    # return {
    # 'statusCode': 200,
    # 'body': json.dumps("Success!!")
# }
#decorator, 
@app.get("/hello")
def hello():
    params = {
        "id": str(uuid.uuid4()),
        "created_dt": str(datetime.datetime.now()),
        "summary": "Action Name",
        "description": "Action Description",
        "priority": "High",
    }
    db_response = dynamo_table().put_item(Item=params)
    # print(db_response)
    return {"read": "hello get!"}

@app.delete("/hello")
def hello_delete():
    return {"delete": "hello delete!"}

@app.patch("/hello")
def hello_patch():
    return {"update": "hello update!"}

def lambda_handler(event, context):
    return app.resolve(event, context)

def dynamo_table():
    table_name = os.environ.get("TABLE", "Actions")
    region = os.environ.get("REGION", "us-east-1")
    aws_environment = os.environ.get("AWSENV", "AWS")
    if aws_environment == "AWS_SAM_LOCAL":
        actions_table = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        actions_table = boto3.resource("dynamodb", endpoint_url="http://localhost:4566", region_name=region)
    return actions_table.Table(table_name)

# curl -X 'POST' http://127.0.0.1:3000/hello/ \
# -H 'Content-Type: application/json' \
# -d '
# {
# "id": 0,
# "name": "string",
# "description": "string"
# }'


# samlocal build && samlocal local start-api

#  curl -X 'PATCH' http://127.0.0.1:3000/hello
# http://localhost:4566/restapis/ja58lkf4pb/local/_user_request_/hello
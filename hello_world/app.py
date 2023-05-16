# import json

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
    return {"read": "hello get!"}

@app.delete("/hello")
def hello_delete():
    return {"delete": "hello delete!"}

@app.patch("/hello")
def hello_patch():
    return {"update": "hello update!"}

def lambda_handler(event, context):
    return app.resolve(event, context)

# curl -X 'POST' http://127.0.0.1:3000/hello/ \
# -H 'Content-Type: application/json' \
# -d '
# {
# "id": 0,
# "name": "string",
# "description": "string"
# }'

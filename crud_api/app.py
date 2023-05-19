import json
import os
import datetime
import uuid

import boto3

from boto3.dynamodb.conditions import Key

from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

# decorator
@app.post("/crud")
def simple_post():
    post_data: dict = app.current_event.json_body
    carro = {
        "id": str(uuid.uuid4()),
        "modelo": post_data['modelo'],
        "marca": post_data['marca'],
        "ano": post_data['ano']
    }
    # salvando pessoa no banco de dados com os atributos já declarados
    db_response = dynamo_table().put_item(Item=carro)
    return {
        "status": "success",
        "data": carro,
        "message": "Item successfully created in the DynamoDB!"
    }, 

# exibe as características dos carros 
@app.get("/crud")
def get_all_data():
    # lendo pessoa do banco de dados usando o nome "a5eec909-e759-4526-875f-56b3bb1fafe8"
    # lendo todo os itens do banco de dados
    db_response = dynamo_table().scan()

    return {
        "status": "success",
        "data": db_response['Items'],
        "message": "Successfully read DynamoDB!"
    }, 200

@app.get("/crud/<id>") # recebendo id por parâmetro
def get_id(id: str):
    # lendo carro do banco de dados filtrando por id "a5eec909-e759-4526-875f-56b3bb1fafe8"
    var = "0"
    if (id):
        var = id
    print(var)
    if(var):
        db_response = dynamo_table().query(KeyConditionExpression=Key('id').eq(var))
    if not db_response['Items']:
        return {
        "status": "not found",
        "data":[],
        "message": "Error id not found!"
        }, 404
    return {
        "status": "success",
        "data": db_response['Items'],
        "message": "Successfully read DynamoDB!"
    }, 200

    # deletar o item e todos os seus atributos de uma vez
@ app.delete("/crud/<id>")
def delete_item(id: str):
    db_response = dynamo_table().delete_item(
        Key={
            'id': id
        }
    )
    return {
        "status": "success",
        "data": [],
        "message": "Successfully deleted item in DynamoDB!"
    }, 200




@ app.patch("/crud")
def update_patch():
    post_data: dict = app.current_event.json_body
    carro = {
        "id": post_data['id'],
        "modelo": post_data['modelo'],
        "marca": post_data['marca'],
        "ano": post_data['ano']
    }
    response = dynamo_table().update_item(
        Key={
            'id': carro['id']
        },
        AttributeUpdates={
            'modelo': {
                "Value": carro['modelo']
            },
            'marca': {
                "Value": carro['marca']
            },
            'ano': {
                "Value": carro['ano']
            }
        }
    )
    return {
        "status": "success",
        "data": carro,
        "message": "Items successfully updated in the DynamoDB!"
    }, 200

def lambda_handler(event, context):
    return app.resolve(event, context)

def dynamo_table():
    table_name = os.environ.get("TABLE", "Actions")
    region = os.environ.get("REGION", "us-east-1")
    aws_environment = os.environ.get("AWSENV", "AWS")
    actions_table = boto3.resource(
        "dynamodb", endpoint_url="http://host.docker.internal:4566")
    # if aws_environment == "AWS_SAM_LOCAL":
    #     actions_table = boto3.resource("dynamodb", endpoint_url="http://host.docker.internal:4566")
    # else:
    #     actions_table = boto3.resource("dynamodb", region_name=region)
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


# awslocal dynamodb put-item --table-name Actions --item '{"id":{"S":"foo"}, "created_dt":{"S":"foo"}}' --region us-east-1

# awslocal dynamodb describe-table --table-name Actions --query 'Table.Replicas' --region us-east-1

# awslocal dynamodb scan --table-name Actions

# Criar a table Actions no start api

# Colocar try catch nas chamadas

# Entender os tipos da tabela do DynamoDB

# HASH - partition key

# RANGE - sort key

# Colocar log na aplicação


# table = boto3.resource('dynamodb').Table('my_table')

# table.update_item(
#     Key={'pkey': 'asdf12345'},
#     AttributeUpdates={
#         'status': 'complete',
#     },
# )

#não esquecer de rodar a url antes de tentar atualizar o codigo, pois é uma func lambida e precisa att.

#ARRUMAR O TRELLO E ATT O WHIMSICAL!!

#Os itens salvos no banco de dados serão carros: 

# carro = {
#     "id": "uuid",
#     "modelo": "modelo_do_carro",
#     "marca": "marca_do_carro"
#     "ano": "ano_de_produção"
# }

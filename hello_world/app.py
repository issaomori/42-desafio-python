import json
import os
import datetime
import uuid

import boto3

from boto3.dynamodb.conditions import Key

from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

# decorator
# --------------------------- P O S T ---------------------------------------
# Salva no banco de dados um item com seus atributos
@app.post("/crud")
def simple_post5442563():
    post_data: dict = app.current_event.json_body
    carro = {
        "id": str(uuid.uuid4()), #id aleatório gerado pela função uuid4 (esse id comporá a chave única do item)
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

# --------------------------- G E T    A L L -----------------------------------
# Exibe todos itens do banco de dados e seus atributos
@app.get("/crud")
def get_all_data436434():
    db_response = dynamo_table().scan()

    return {
        "status": "success",
        "data": db_response['Items'],
        "message": "Successfully read DynamoDB!"
    }, 200

# --------------------------- G E T    I T E M ---------------------------------
# procura e exibe os atributos um item baseado no id passado por parâmetro na URL
@app.get("/crud/<id>") # recebendo id por parâmetro
def get_id34534(id: str):
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

# --------------------------- D E L E T E -----------------------------------
# deletar o item e todos os seus atributos de uma vez
@ app.delete("/crud/<id>")
def delete_item53543(id: str):
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

# --------------------------- U P D A T E-----------------------------------
# atualiza um item e todos os seus atributos de uma vez, se o ID não existir, cria-se o item já atualizado
@ app.patch("/crud")
def update_patch23343():
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

# --------------------------- C O N F I G -----------------------------------
# Onde criamos as rotas e a API
def lambda_handler(event, context):
    return app.resolve(event, context)

# Função auxiliar que configura o boto3 em interação com o DynamoDB
def dynamo_table():
    table_name = os.environ.get("TABLE", "Actions")
    region = os.environ.get("REGION", "us-east-1")
    aws_environment = os.environ.get("AWS_SAM_LOCAL", "AWS")
    # actions_table = boto3.resource(
        # "dynamodb", endpoint_url="http://host.docker.internal:4566")
    if aws_environment == "AWS_SAM_LOCAL":
        actions_table = boto3.resource("dynamodb", endpoint_url="http://host.docker.internal:4566")
    else:
        actions_table = boto3.resource("dynamodb", region_name=region)
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

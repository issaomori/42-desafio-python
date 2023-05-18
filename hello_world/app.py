import json
import os
import datetime
import uuid

import boto3

from boto3.dynamodb.conditions import Key

from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

# declaração do ITEM pessoa e de seus atributos
pessoa = {
    "id": "1",
    "nome": "José",
    "idade": "28"
}

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
# decorator,

# exibe as características das pessoas 
@app.get("/hello")
def hello():
    pessoa = {
        "id": "2",
        "nome": "Maria"
    }
    # salvando pessoa no banco de dados com os atributos já declarados
    db_response = dynamo_table().put_item(Item=pessoa)

    # lendo pessoa do banco de dados
    # response = dynamo_table().get_item(
    # Key={
    #     "id": "1",
    #     "nome": "José"
    # }
    # )

    # lendo pessoa do banco de dados usando o nome
    # response = dynamo_table().query(KeyConditionExpression=Key('id').eq('1'))

    # lendo todo os itens do banco de dados
    # response = dynamo_table().scan()

    # atualizar pessoa
    #  -um item especifico.
    #  -todos os itens de uma só vez.
    # response = dynamo_table().update_item(
    #     Key={
    #         'id': '1'
    #     },
    #     UpdateExpression='SET nome = :newNome',
    #     ExpressionAttributeValues={
    #         ':newNome': "Paulo"
    #     },
    #     ReturnValues="UPDATED_NEW"
    # )
    # response = dynamo_table().update_item(
    #     Key={
    #         'id': '2'
    #     },
    #     AttributeUpdates={
    #         'nome': {
    #             "Value": "Marcelo"
    #         }
    #     }
    # )

    # deletar pessoa (item) e todos os seus atributos
    response = dynamo_table().delete_item(
        Key={
            'id': '1'
        }
    )

    # print(response)
    # print(response)
    # print(db_response)
    # return {"read": json.dumps(response['Items'])}
    return {"read": "hello get"}


@ app.delete("/hello")
def hello_delete():
    return {"delete": "hello delete!"}


@ app.patch("/hello")
def hello_patch():
    return {"update": "hello update!"}


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
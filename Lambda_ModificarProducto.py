import boto3
import json

def lambda_handler(event, context):
    print(event)
    # Entrada (json)
    producto = event['body']
    
    # Inicio - Proteger el Lambda
    token = event['headers']['Authorization']
    lambda_client = boto3.client('lambda')    
    payload_string = '{ "token": "' + token +  '" }'
    invoke_response = lambda_client.invoke(FunctionName="ValidarTokenAcceso",
                                           InvocationType='RequestResponse',
                                           Payload = payload_string)
    response = json.loads(invoke_response['Payload'].read())
    print(response)
    if response['statusCode'] == 403:
        return {
            'statusCode' : 403,
            'status' : 'Forbidden - Acceso No Autorizado'
        }
    # Fin - Proteger el Lambda        

    # Proceso
    client = boto3.client('dynamodb')
    response = client.query(
        TableName='t_productos',
        KeyConditionExpression='tenant_id=:tenant_id AND producto_id=:producto_id',
        ExpressionAttributeValues={
            ":tenant_id": {"S": tenant_id},
            ":producto_id": {"S": producto_id}
        }
    )
    if response['Count'] == 0:
        return {
            'statusCode' : 400,
            'status' : 'Bad Request - Producto no existe'
        }

    response = client.update_item(
        TableName='t_productos',
        KeyConditionExpression='tenant_id=:tenant_id AND producto_id=:producto_id',
        ExpressionAttributeValues={
            ":tenant_id": {"S": tenant_id},
            ":producto_id": {"S": producto_id}
        }
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'response': producto
    }

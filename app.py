import json

# from tests.test_ifcGirder import test_Ifc
from src.ifcGirder import createIfcGirder

def lambda_handler(event, context):

    result = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }

    # GET
    if not 'body' in event:
        result["body"] = "helloworld"
        return result

    # POST
    palam = event['body']
    result["body"] = createIfcGirder(palam)
    return result


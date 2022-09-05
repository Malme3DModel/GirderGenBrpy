import json

# from tests.test_ifcGirder import test_Ifc
from src.ifcGirder import createIfcGirder

def lambda_handler(event, context):

    # GET
    if not 'body' in event:
        return "helloworld"

    # POST
    palam = event['body']
    ifcStr = createIfcGirder(palam)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": ifcStr,
            }
        ),
    }


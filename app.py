import json

from tests.test_ifcGirder import test_Ifc

def lambda_handler(event, context):

    print(f"Looks like requests, context {context}")

    ifcStr = test_Ifc()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": ifcStr,
            }
        ),
    }


import json

from tests.test_ifcGirder import test_Ifc

def lambda_handler(event, context):

    print(f"lambda_handler calling, context: {context}")

    ifcStr = test_Ifc()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": ifcStr,
            }
        ),
    }


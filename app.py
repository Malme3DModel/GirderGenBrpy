import json

# from tests.test_ifcGirder import test_Ifc

def handler(event, context):

    # ifcStr = test_Ifc()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "ifcStr",
            }
        ),
    }
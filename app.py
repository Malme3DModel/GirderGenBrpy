import json
import pandas as pd
import requests
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


def lambda_handler(event, context):
    print(f"Looks like pandas is installed, version {pd.__version__}")
    print(f"Looks like requests is installed, version {requests.__version__}")

    return "Hello World"

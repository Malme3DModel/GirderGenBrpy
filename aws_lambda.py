import json as json2

# from tests.test_ifcGirder import test_Ifc
from src.ifcGirder import createIfcGirder

def lambda_handler(event, context):

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Content-Encoding',
        'Access-Control-Max-Age': '3600'
    }

    # 3Dモデルを作成する
    try:
        from src.ifcGirder import createIfcGirder

        body = event['body']
        ifcGirder = createIfcGirder(body)

        return (json2.dumps({ 'body': ifcGirder}), 200, headers)

    except:
        return (json2.dumps({'body': 'err'}), 500, headers)
from flask import Flask, url_for, request, redirect
app = Flask(__name__)

import json


# POSTメソッドでデータが送信された場合の処理
@app.route('/', methods=['OPTIONS', 'GET', 'POST'])
def post():

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Content-Encoding',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    result = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }

    if request.method == 'GET':
        return (json.dumps({ 'results': 'Hello World!'}), 200, headers) # テスト用コード

    # リクエストから「body」を取得
    event = request.get_json() 
    if not 'body' in event:
        result["body"] = 'error! "palam" not found.'
        return result


    # 3Dモデルを作成する
    from src.ifcGirder import createIfcGirder
    palam = event['body']
    result["body"] = createIfcGirder(palam)
    return result

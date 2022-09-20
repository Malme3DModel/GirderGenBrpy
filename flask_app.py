from flask import Flask, url_for, request, redirect
app = Flask(__name__)

import json


# POSTメソッドでデータが送信された場合の処理
@app.route('/', methods=['OPTIONS', 'GET', 'POST'])
def post():

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Content-Encoding',
        'Access-Control-Max-Age': '3600'
    }

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        return ('', 204, headers)


    if request.method == 'GET':
        return (json.dumps({ 'body': 'Hello World!'}), 200, headers) # テスト用コード


    # 3Dモデルを作成する
    try:
        from src.ifcGirder import createIfcGirder

        event = request.get_json() 
        body = event['body']
        ifcGirder = createIfcGirder(body)

        return (json.dumps({ 'body': ifcGirder}), 200, headers)

    except:
        import traceback
        traceback.print_exc()
        return (json.dumps({ 'body': traceback.print_exc()}), 500, headers)


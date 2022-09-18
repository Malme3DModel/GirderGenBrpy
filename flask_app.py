from flask import Flask, url_for, request, redirect
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello, World!"


# POSTメソッドでデータが送信された場合の処理
@app.route('/', methods=['POST'])
def post():

    result = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }

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

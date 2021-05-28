from parser import main
from flask import Flask, request

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'


HTTP_OK_CODE = 200
HTTP_ERROR_CODE = 400
HTTP_PAGE_NOT_FOUND_CODE = 404


@app.route("//api/v1?method=<method_name>&profile=<username>", methods=["GET"])
def get_all_company_data(method_name, username):
    pass

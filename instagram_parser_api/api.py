

from .parser import main
from flask import Flask, request
import logging
import json
import sys
import os


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'


HTTP_OK_CODE = 200
HTTP_ERROR_CODE = 400
HTTP_PAGE_NOT_FOUND_CODE = 404

host_username = os.getenv('HOST_USERNAME', 'bozzyk44')
host_password = os.getenv('HOST_PASSOWRD', 'Zsedcvbnm@#$')


def _pack_raw(content, status_code=HTTP_OK_CODE):
    return json.dumps(content), status_code


@app.route("/api/v1", methods=["GET"])
def get_info():
    username = request.args['profile']
    method = request.args['method']
    logging.info(f'Request for {method} for username: {username}')
    data = main(host_username, host_password, username, method)
    return _pack_raw(data)


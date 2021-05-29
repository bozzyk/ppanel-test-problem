import logging
import json
import sys
import os

from flask import Flask, request

from .parser import main


logging.basicConfig(filename='log.txt', filemode='a', datefmt='%H:%M:%S', level=logging.DEBUG)
running_requests = []

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'


host_username = os.getenv('HOST_USERNAME')
host_password = os.getenv('HOST_PASSWORD')


def _pack_raw(content, status_code=200):
    return json.dumps(content), status_code


@app.route("/api/v1", methods=["GET"])
def get_info():
    ip = request.remote_addr
    logging.info(f'Request from IP {ip} recieved')
    if ip in running_requests:
        logging.info(f'Rejected request from {ip} - simultaneous requests from single IP are not allowed')
        return _pack_raw({'error': 'Too many requests'})
    running_requests.append(ip)
    username = request.args['profile']
    method = request.args['method']
    logging.info(f'Request parameters: method = {method}, username = {username}')
    try:
        data = main(host_username, host_password, username, method)
    except Exception:
        data = None
    running_requests.remove(ip)
    if not data:
        return _pack_raw({
            "status": "error",
            "code": 403,
            "message": "Invalid account name"
        }, 403)   
    return _pack_raw({
        'status': 'success',
        'code': 200,
        'data': data
    })


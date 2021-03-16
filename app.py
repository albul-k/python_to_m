import mg_python
import json
from flask import Flask, request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return mg_python.m_ext_version()

@app.route('/table', methods=['GET'])
def test():    
    json_data = mg_python.m_function(0, "table^API")
    res = make_response(json.loads(json_data), 200)
    return res

@app.route('/set', methods=['GET'])
def set():
    global_name = request.args.get('global')
    key = request.args.get('key')
    value = request.args.get('value')

    mg_python.m_set(0, global_name, key, value)
    
    return 'Success'

@app.route('/get', methods=['GET'])
def get():
    global_name = request.args.get('global')
    key = request.args.get('key')
    
    return mg_python.m_get(0, global_name, key)

@app.route('/order', methods=['GET'])
def order():
    global_name = request.args.get('global')
    key = mg_python.m_order(0, global_name, "")
    result = str()
    while (key != ""):
        result += f'key={key}, value={mg_python.m_get(0, global_name, key)}<br/>'
        key  = mg_python.m_order(0, global_name, key)
    
    return result

if __name__ == '__main__':
    mg_python.m_set_host(0, "localhost", 7041, "", "")
    mg_python.m_set_uci(0, "QMS")
    mg_python.m_bind_server_api(0, "Cache", "C:\InterSystems\Cache\mgr", "_SYSTEM", "SYS", "", "")
    app.run()
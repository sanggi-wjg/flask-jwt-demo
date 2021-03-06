import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask import _app_ctx_stack as ctx_stack

from demo.decorators import jwt_required
from demo.jwt_builder import encode_jwt, get_jwt_identity

app = Flask("Flask-JWT-Demo")
app.config["ENV"] = "local"
app.config["DEBUG"] = True
app.config["JWT_SECRET_KEY"] = "secret-key"

app.config['JWT_HEADER_ALG'] = 'HS256'
app.config['JWT_HEADER_TYP'] = 'JWT'
app.config['JWT_PAYLOAD_EXP_DELTA'] = 8


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico", mimetype = "image/vnd.microsoft.icon")


@app.route("/", methods = ["GET"])
def hello():
    return render_template("login.html")


@app.route("/login", methods = ["POST"])
def login():
    if not request.is_json:
        return jsonify({ "msg": "Missing JSON in request" }), 400

    req_json = request.get_json()
    userid = req_json.get("userId")
    password = req_json.get("password")

    if not userid:
        return jsonify({ "msg": "Empty userId" }), 400
    if not password:
        return jsonify({ "msg": "Empty password" }), 400

    if userid != "test" or password != "123":
        return jsonify({ "msg": "Invalid userId or password" }), 401

    jwt = encode_jwt(userid)
    return jsonify({ "token": jwt }), 200


@app.route("/protected", methods = ['POST'])
@jwt_required
def protected():
    return jsonify({ "msg": get_jwt_identity() }), 200


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8085)

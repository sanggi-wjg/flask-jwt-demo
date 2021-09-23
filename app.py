import os

from flask import Flask, render_template, request, redirect, jsonify, send_from_directory

from jwt.decorators import jwt_required

app = Flask("Flask-JWT-Demo")
app.config["ENV"] = "local"
app.config["DEBUG"] = True
app.config["JWT_SECRET_KEY"] = "secret-key"


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

    if userid != "test" or password != "test":
        return jsonify({ "msg": "Invalid userId or password" }), 400

    return jsonify({ "msg": "Success" }), 200


@app.route("/protected", methods = ['POST'])
@jwt_required
def protected():
    return jsonify({ "msg": "Success" }), 200


if __name__ == "__main__":
    app.run()

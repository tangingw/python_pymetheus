from flask import Flask, abort, jsonify, request

app = Flask(__name__)


@app.errorhandler(403)
def return_forbidden_page(error):

    return jsonify(
        status=403, message="Forbidden Request"
    ), 403


@app.route("/")
def return_index():
    # This is for debugging
    return jsonify(
        {
            "message": "Hello World!"
        }
    )


@app.route("/collect", methods=["GET", "POST"])
def collect_data():

    if request.method == "POST":

        if request.is_json:

            return jsonify(request.get_json())
        
    abort(403)

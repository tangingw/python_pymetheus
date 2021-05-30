import time
from queue import Queue

from flask import Flask, abort, jsonify, request
#from flask import redirect, url_for


flask_queue = Queue()
processed_queue = Queue()

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

    if request.method == "POST" and request.is_json:        
        """to be replaced with DB or ZeroMQ"""
        return jsonify(request.get_json())
        
    abort(403)


@app.route("/heartbeat", methods=["GET", "POST"])
def get_heartbeat():

    if request.method == "POST" and request.is_json:
        """to be replaced with DB or ZeroMQ"""
        return jsonify(request.get_json())
    
    abort(403)


@app.route("/collect_new", methods=["GET", "POST"])
def collect_queue_data():

    if request.method == "POST" and request.is_json:

        current_time = int(time.time() * 1000)
        current_data = {
            "id": current_time,
            "data": request.get_json()
        }


        flask_queue.put(current_data)
        
        return jsonify(
            {
                "status_code": 200,
                "result_page": f"get_data/{current_time}"
            }
        )

        #return redirect(f"get_data/{current_time}", code=302)

    abort(403)


@app.route("/get_data/<my_id>")
def get_data(my_id):

    index = 0
    current_queue_length = processed_queue.qsize()
  
    while (processed_queue.not_empty and index < current_queue_length):

        temp_data = processed_queue.get()

        if temp_data["id"] == int(my_id):

            return jsonify(temp_data)
        
        flask_queue.put_nowait(temp_data)
        index += 1

    return jsonify(
        {
            "status_code": 404,
            "status_msg": f"{my_id}: data not found or not ready"
        }
    )
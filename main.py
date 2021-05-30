from time import thread_time
from app import app
from daemon_task import worker_task_daemon
from app import flask_queue
from app import processed_queue


if __name__ == "__main__":

    worker_task_daemon(flask_queue, processed_queue, thread_num=50)    
    app.run("0.0.0.0", port=5000, debug=True, threaded=True)
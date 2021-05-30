import json
import requests
import threading
from queue import Queue


def submit_my_job(my_device_data, queue):
    response = requests.post(
        "http://127.0.0.1:5000/collect_new",
        json=my_device_data
    )

    queue.put_nowait(response.text)

my_queue = Queue()

testing_data_list = [
    {
        "device": f"my device {index}",
        "ip_address": f"192.168.0.{index}",
        "status_code": 200,
        "status_msg": "I am safe"
    } for index in range(1, 200)
]

threading_list = [
    threading.Thread(
        target=submit_my_job, args=(testing_data, my_queue)
    ) for testing_data in testing_data_list
]

for thread in threading_list:
    thread.start()

for thread in threading_list:
    thread.join()


def fetch_data(task_result):

    print(task_result)
    if task_result["status_code"] == 200:
        
        response = requests.get("http://127.0.0.1:5000/{0}".format(task_result["result_page"]))
        response_data = json.loads(response.text)

        while response_data["status_code"] == 404:

            response = requests.get("http://127.0.0.1:5000/{0}".format(task_result["result_page"]))
            print(response.text, type(response.text))
            response_data = json.loads(response.text)
        
        print(response_data)


while not my_queue.empty():
    
    if my_queue.empty:
        print("Y")

    task_result = json.loads(my_queue.get())
    
    my_thread = threading.Thread(target=fetch_data, args=(task_result,))
    my_thread.start()

    

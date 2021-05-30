import time
import threading


def get_task(received_queue, processed_queue):

    while True:

        if received_queue.not_empty:
            task = received_queue.get()
            print(task)
            time.sleep(0.5)

            task.update({"status_code": 200})
            processed_queue.put(task)


def worker_task(received_queue, processed_queue, thread_num=5):

    worker_thread_list = [
        threading.Thread(target=get_task, args=(received_queue, processed_queue))
        for _ in range(thread_num)
    ]

    for worker_thread in worker_thread_list:

        worker_thread.start()


def worker_task_daemon(received_queue, processed_queue, thread_num=5):

    daemon_thread = threading.Thread(
        target=worker_task, args=(received_queue, processed_queue, thread_num),
        daemon=True
    )

    daemon_thread.start()
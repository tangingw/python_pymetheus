import psutil

current_process = {process.pid: process for process in psutil.process_iter(['pid', 'name', 'username'])}
for p in psutil.net_connections():

    if p.pid in current_process.keys():

        print(p, current_process[p.pid])
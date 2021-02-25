from datetime import datetime
import requests
from monitor_platform import MonitorPlatform
from monitor_sys import MonitorCPU, MonitorDisk, MonitorMemory


export_data = {
    "datetime": datetime.utcnow().isoformat(),
    "identifier": ["device"]
}

export_data.update(
    {
        "platform": MonitorPlatform().get_platform_info()
    }
)
export_data.update(
    {
        "cpu": MonitorCPU().get_cpu_data()
    }
)

export_data.update(
    {
        "disk": MonitorDisk().get_disk_all_data()
    }
)

export_data.update(
    {
        "memory": MonitorMemory().get_memory_data()
    }
)

response = requests.post(
    "http://127.0.0.1:5000/collect", json=export_data
)

print(
    response.status_code, response.text
)

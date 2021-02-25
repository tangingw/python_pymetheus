import psutil
from datetime import datetime
from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM


def get_network_interface():

    ip_layer_dict = {
        AF_INET: "ipv4",
        AF_INET6: "ipv6"
    }

    network_interface_info = psutil.net_if_addrs()
    network_interface_dict = {
        interface_name: [
            {
                "ip_type": ip_layer_dict[intf.family] if intf.family in ip_layer_dict.keys() else "mac-address",
                "mac_address": intf.address if intf.family not in ip_layer_dict.keys() else None,
                "ip_address": intf.address if intf.family in ip_layer_dict.keys() else None,
                "netmask": intf.netmask, "broadcast": intf.broadcast
            } for intf in interfaces
        ] for interface_name, interfaces in network_interface_info.items()
    }
    
    return network_interface_dict


def get_connection_process():

    protocol_dict = {
        (AF_INET, SOCK_DGRAM): "udp",
        (AF_INET6, SOCK_DGRAM): "udp6",
        (AF_INET6, SOCK_STREAM): "tcp6",
        (AF_INET, SOCK_STREAM): "tcp"
    }

    connection_process = []
    current_process = {
        process.pid: process for process in psutil.process_iter(['pid', 'name', 'username'])
    }

    for p in psutil.net_connections(kind="inet"):

        if p.pid in current_process.keys():

            local_addr = f"{p.laddr.ip}:{p.laddr.port}"
            remote_addr = f"{p.raddr.ip}:{p.raddr.port}" if p.raddr else "-"

            connection_process.append(
                {
                    "process_name": current_process[p.pid].info["name"],
                    "status": current_process[p.pid].status(),
                    "started_at": datetime.fromtimestamp(
                        current_process[p.pid].create_time()
                    ).isoformat(),
                    "protocol": protocol_dict[(p.family, p.type)],
                    "local_address": local_addr,
                    "remote_address": remote_addr
                }
            )
    
    return connection_process


print(
    get_network_interface()
)
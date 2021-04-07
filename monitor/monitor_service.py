import socket
import requests


class MonitorService:

    def __init__(self, service_port, service_proto, service_desc=None):

        self.service_desc = service_desc
        self.service_port = service_port
        self.service_proto = service_proto
    
    def get_service_metadata(self):

        return {
            "service_desc": self.service_desc,
            "service_port": self.service_port,
            "service_proto": self.service_proto
        }

    def get_status(self):
        """
        To be overriden by daughter class
        """
        pass


class MonitorHTTP(MonitorService):

    def __init__(self, http_url, service_desc=None, service_port=80):

        self.http_url = http_url
        super().__init__(service_port, "http", service_desc)

    def get_status(self, headers=None, params=None):

        try:
            service_response = requests.get(self.http_url, headers=headers, params=params)
        
        except requests.exceptions.ConnectionError as error_msg:

            return {
                "status_code": 500,
                "error_message": error_msg
            }
        
        else:

            return {
                "status_code": service_response.status_code,
                "service_body": service_response.text
            }


class MonitorDBMS(MonitorService):

    def __init__(self, dbms_connection, service_port, service_desc=None):

        self.dbms_connection = dbms_connection
        super().__init__(service_port, "tcp", service_desc)
    
    def get_status(self):

        return 



class MonitorPort(MonitorService):

    def __init__(self, ip_address, service_port, service_proto="tcp", service_desc=None):

        self.ip_address = ip_address
        super().__init__(service_port, service_proto, service_desc)
    
    def get_status(self):

        socket_proto_type = socket.SOCK_STREAM
        
        if self.service_proto == "udp":

            socket_proto_type = socket.SOCK_DGRAM

        socket.setdefaulttimeout(1)
        sock_connection = socket.socket(socket.AF_INET, socket_proto_type)

        try:
            sock_connection.connect((self.ip_address, int(self.service_port)))

        except (ConnectionRefusedError, TimeoutError, OSError):

            return "failed"

        else:

            return "success"
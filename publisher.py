from .conf import UDP_DEFAULT_IP, UDP_DEFAULT_PORT, UDP_MAX_LEN

import socket

class Publisher:
    def __init__(self, topic, ip=UDP_DEFAULT_IP, port=UDP_DEFAULT_PORT):
        self.topic = topic
        self.ip = ip
        self.port = port
        self.__sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_string(self, data: str) -> bool:
        return self.send_bytes(str.encode(data))

    def send_bytes(self, data: bytes) -> bool:
        packet_len = len(self.topic) + 1 + len(data)
        if packet_len >= UDP_MAX_LEN:
            return False
        buffer = str.encode(self.topic + '\0') + data
        bytes_sent = self.__sock.sendto(buffer, (self.ip, self.port))
        return bytes_sent == packet_len

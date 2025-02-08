from .conf import UDP_DEFAULT_IP, UDP_DEFAULT_PORT, UDP_MAX_LEN

import socket

class Subscriber:
    def __init__(self, topic, ip=UDP_DEFAULT_IP, port=UDP_DEFAULT_PORT):
        self.topic = topic
        self.ip = ip
        self.port = port
        self.__sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.ip, self.port))

    def recv(self) -> bool:
        try:
            packet = self.__sock.recv(UDP_MAX_LEN, socket.MSG_DONTWAIT)
        except BlockingIOError as e:
            return False
        recv_topic, recv_data = packet.split(b'\0', 1)
        recv_topic = recv_topic.decode()
        if self.__topic_matches(recv_topic):
            self.recv_topic = recv_topic
            self.recv_data = recv_data
            return True
        return False

    def __topic_matches(self, topic) -> bool:
        if self.topic.endswith("*") and len(topic) > len(self.topic):
            substr_len = len(self.topic[:-1])
            return topic[:substr_len] == self.topic[:-1]
        return topic == self.topic

    def get_recv_topic(self) -> str:
        return self.recv_topic

    def get_string(self) -> str:
        return self.recv_data.decode()

    def get_bytes(self) -> bytes:
        return self.recv_data

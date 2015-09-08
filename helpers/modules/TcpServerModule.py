from helpers.modules.BaseModule import BaseModule

import random
import socket
import threading


class TcpServerModule(BaseModule):
    clients = {}
    server_ip = '127.0.0.1'
    server_port = 0
    allowned_ip = []

    def client_disconected(self, ip, port, client_key):
        """Client disconected"""
        pass

    def close_client(self, client_key):
        """Close socket client"""
        if client_key not in self.clients:
            return False

        self.clients[client_key]['socket'].close()

    def new_client(self, socket, ip, port, client_key):
        """New client connected"""
        pass

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.server_ip, self.server_port))
        self.server.listen(0)

        # random free port
        if self.server_port == 0:
            self.server_port = self.server.getsockname()[1]

        while self.is_running:
            client_socket, client_addr = self.server.accept()
            ip, port = client_addr

            # ip allowned ?
            if self.allowned_ip and ip not in self.allowned_ip:
                client_socket.close()
                self.add_warning('Client %s not allowned' % ip)
                continue

            threading.Thread(
                None,
                self.__client_thread,
                'module: %s tcp_client: %s:%s' % (self.module_name, ip, port),
                (client_socket, ip, port)
            ).start()

    def receive(self, data, client_key):
        """New message from client"""
        pass

    def send(self, message, client_key):
        """Send message to client"""

        if client_key not in self.clients:
            return False


        self.clients[client_key]['socket'].send(message.encode())

    def stopped(self):
        for client_key in self.clients:
            self.send('module %s has been stopped' % self.module_name, client_key)
            self.close_client(client_key)

        self.server.close()

    def __client_thread(self, socket, ip, port):
        client_key = '%030x' % random.randrange(16**30)
        self.clients[client_key] = {
            'socket': socket,
            'ip': ip,
            'port': port,
        }
        self.new_client(socket, ip, port, client_key)

        while socket and self.is_running:
            try:
                data = socket.recv(1024)
                self.receive(data, client_key)
            except OSError:
                break

        self.client_disconected(ip, port, client_key)
        del self.clients[client_key]
        socket.close()
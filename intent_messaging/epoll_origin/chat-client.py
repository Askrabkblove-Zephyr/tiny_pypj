"""
MIT License

Copyright (c) 2025 Askrabkblove-Zephyr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import socket
import select
import sys
class ChatClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.epoll = select.epoll()

    def chat_client(self):
        # 注册连接到epoll
        self.epoll.register(self.client_socket.fileno(), select.POLLIN)
        self.epoll.register(sys.stdin.fileno(), select.POLLIN)
        while True:
            events = self.epoll.poll(-1)
            for fd, event in events:
                if fd == sys.stdin.fileno():
                    data = input("You: ")
                    self.client_socket.send(data.encode('utf-8'))
                elif fd == self.client_socket.fileno():
                    data = self.client_socket.recv(1024).decode('utf-8')
                    if data:
                        print(data)
                    else:
                        print("服务器断开链接")
                        return


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9000
    chat_client = ChatClient(host, port)
    chat_client.chat_client()
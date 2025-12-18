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

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 即使服务器关闭了，TCP连接可能还处于 TIME_WAIT 状态（通常2分钟），操作系统不允许立即重用相同的地址和端口。
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        self.epoll = select.epoll() # select标准库的epoll

    def chat(self):
        conn, addr = self.sock.accept() # 从Accept队列中取出已经完成三次握手的连接
        print("Connected by", addr)
        print("Connected by", conn)
        # POLLIN 是 可读事件标志，表示"文件描述符上有数据可读"。
        self.epoll.register(conn.fileno(), select.POLLIN) # 注册连接到epoll
        # file descriptor number
        self.epoll.register(sys.stdin.fileno(), select.POLLIN)
        '''
            服务器终端（用户）      服务器程序         客户端
            你: Hello↵          → input()返回"Hello"
                                → sendall("Hello") → 客户端收到"Hello"
                                                   ← 客户端用户输入"Hi there!"
                                ← recv()收到"Hi there!"
            显示: Hi there!     ← print("Hi there!")
            
            你: How are you?↵   → input()返回"How are you?"
                                → sendall("How are you?") → ...
        '''
        while True:
            events = self.epoll.poll(-1) # 等待事件发生
            print(events)
            for fileno, event in events:
                # 标准输入里面有数据了
                if fileno == sys.stdin.fileno():
                    # 第一步：input() 会阻塞等待用户在终端输入
                    data = input()  # ❌ 这里是等**用户**在服务器终端输入，不是接收客户端数据！

                    # 第二步：把用户的输入发送给客户端
                    conn.sendall(data.encode('utf-8'))  # 发送给客户端
                # 如果socket链接有数据了
                elif fileno == conn.fileno():
                    # 第三步：接收客户端回复
                    data = conn.recv(1024).decode('utf-8')  # 接收客户端数据
                    if data:
                        # 第四步：打印客户端的回复
                        print(data)  # 显示在服务器终端
                    else:
                        print("客户端断开连接")
                        return
if __name__ == '__main__':
    server = ChatServer('127.0.0.1', 9000)
    server.chat()
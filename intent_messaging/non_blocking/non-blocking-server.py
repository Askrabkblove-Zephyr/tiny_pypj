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

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = ('127.0.0.1', 9000)
tcp_server_socket.bind(address)
tcp_server_socket.listen(100)
tcp_server_socket.setblocking(False)

client_socket = None

while True:
    # 接受新连接
    try:
        client_socket, client_addr = tcp_server_socket.accept()
        print(f"客户端连接: {client_addr}")
        client_socket.setblocking(False)
    except BlockingIOError:
        # 没有新连接，继续
        print('waiting for connection...')
        pass

    # 如果有客户端连接，处理数据
    if client_socket:
        try:
            text = client_socket.recv(1024)
            # 如果对方断开
            if not text:
                print('byebye')
                client_socket = None  # 重置，等待新连接
            else:
                print(text.decode('utf-8'))
        except BlockingIOError:
            # 没有数据可读，继续
            print('waiting for data...')
            pass
        except Exception as e:
            print(f"错误: {e}")
            client_socket = None
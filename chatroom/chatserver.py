import socket
import threading

# 创建套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器地址和端口
server_address = ('192.168.199.59', 5555)
server_socket.bind(server_address)

# 监听连接
server_socket.listen(5)
print('服务器正在监听连接...')

# 用于存储连接到服务器的客户端
clients = []

def handle_client(client_socket, client_address, username):
    try:
        # 向所有客户端广播新连接消息
        for c in clients:
            c[0].send(f"[USERLIST] {' '.join([client[2] for client in clients])}".encode('utf-8'))

        # 处理客户端消息
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # 广播消息给所有客户端
            for c in clients:
                c[0].send(f"{username}: {message}".encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 移除断开连接的客户端
        clients.remove((client_socket, client_address, username))
        client_socket.close()

        # 向所有客户端广播离开消息
        for c in clients:
            c[0].send(f"[USERLIST] {' '.join([client[2] for client in clients])}".encode('utf-8'))

# 不断接受新连接
while True:
    client_socket, client_address = server_socket.accept()
    print(f"新连接：{client_address}")

    # 获取用户名
    username = client_socket.recv(1024).decode('utf-8')

    # 将新连接的客户端添加到列表
    clients.append((client_socket, client_address, username))

    # 创建新线程处理客户端
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
    client_handler.start()

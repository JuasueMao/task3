import socket

def reverse_text(text):
    return text[::-1]

def handle_client(client_socket):
    while True:
        # 接收初始化报文
        init_msg = client_socket.recv(6)
        if not init_msg:
            break

        msg_type, num_blocks = int(init_msg[:2]), int(init_msg[2:].decode())
        if msg_type != 1:
            print("Invalid message type")
            break

        # 发送 agree 报文
        client_socket.send(b'02')

        for i in range(num_blocks):
            # 接收 reverseRequest 报文
            request_msg = client_socket.recv(6)
            if not request_msg:
                break
            msg_type, data_length = int(request_msg[:2]), int(request_msg[2:6].decode())
            if msg_type != 3:
                print("Invalid message type for reverseRequest")
                break

            data = client_socket.recv(data_length).decode()

            # 反转数据并发送 reverseAnswer 报文
            reversed_data = reverse_text(data)
            response_msg = f"04{data_length:04}".encode() + reversed_data.encode()
            client_socket.send(response_msg)

            # 打印反转结果
            print(f"Received reversed block {i + 1}: {reversed_data}")

    client_socket.close()

def main():
    server_ip = "127.0.0.1" #"192.168.109.129"
    server_port = 31125

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print("Server listening on {}:{}".format(server_ip, server_port))

    while True:
        client_socket, addr = server.accept()
        print("Accepted connection from {}".format(addr))
        handle_client(client_socket)

if __name__ == "__main__":
    main()

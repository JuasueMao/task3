import socket
import random

def main():
    server_ip ="192.168.109.129"#127.0.0.1
    server_port = 31125
    input_file = "D:\\campus\\network\\课设\\input.txt"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    with open(input_file, 'r') as file:
        data = file.read().replace('\n', ' ').strip()  # 移除多余的换行符并去掉前后的空白

    file_length = len(data)
    Lmin = 5   # 最小块长度
    Lmax = 500  # 最大块长度

    if file_length < Lmin:
        print("File length is less than minimum block size.")
        client.close()
        return

    blocks = []
    total_length = 0

    while total_length < file_length:
        if total_length + Lmin >= file_length:  # 如果剩余部分小于最小块长度，则全部作为最后一块
            block_length = file_length - total_length
        else:
            max_block_length = min(Lmax, file_length - total_length)
            block_length = random.randint(Lmin, max_block_length)

        block = data[total_length:total_length + block_length].strip()  # 移除块前后的空白
        blocks.append(block)
        total_length += block_length

    num_blocks = len(blocks)

    # 发送 Initialization 报文 (Type = 1)
    init_msg = f"01{num_blocks:04}".encode()
    client.send(init_msg)

    # 接收 agree 报文 (Type = 2)
    agree_msg = client.recv(2)
    if agree_msg != b'02':
        print("Did not receive agreement from server")
        client.close()
        return

    for i, block in enumerate(blocks):
        block_length = len(block)
        # 发送 reverseRequest 报文 (Type = 3)
        request_msg = f"03{block_length:04}".encode() + block.encode()
        client.send(request_msg)

        # 接收 reverseAnswer 报文 (Type = 4)
        response_msg = client.recv(6)
        msg_type, data_length = int(response_msg[:2]), int(response_msg[2:6].decode())
        reversed_data = client.recv(data_length).decode()

        print(f"Received reversed block {i + 1}: {reversed_data}")

    client.close()

if __name__ == "__main__":
    main()

import os
import socket
import uuid
from stage1.config import Config

class TcpServer:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((Config.SERVER_ADDRESS, Config.SERVER_PORT))




def main():
    tcp_server = TcpServer()
    tcp_server.socket.listen(1)
    try:
        while True:
            connection, client_address = tcp_server.socket.accept()
            file_size = int.from_bytes(connection.recv(32), byteorder='big')
            if file_size <= 0:
                raise Exception('No data')

            save_file = os.path.join(Config.SERVER_FILE, str(uuid.uuid4()) + '.mp4')
            with open(save_file, 'wb+') as f:
                decrement_file_size = file_size
                while decrement_file_size > 0:
                    chunk = connection.recv(decrement_file_size if decrement_file_size < Config.MP4_MAX_STREAM_BYTES else Config.MP4_MAX_STREAM_BYTES)
                    f.write(chunk)
                    decrement_file_size -= Config.MP4_MAX_STREAM_BYTES
            
            connection.send('upload completed.'.ljust(16, '\x00').encode('utf-8'))
            print('complate upload')
    except Exception as e:
        print('error: ' ,e)
    finally:
        connection.close()

main()
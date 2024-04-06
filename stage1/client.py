import os
import socket
from stage1.config import Config

class TcpClient:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((Config.SERVER_ADDRESS, Config.SERVER_PORT))
    

class Mp4FileUploadClient:
    def __init__(self) -> None:
        self.file_path = ''
        self.file_size = 0

    def file_validate(self, input_file_path: str) -> bool:
        #ファイルパスの存在
        if(not(os.path.isfile(input_file_path))): return False
        #ファイルの形式が正しいか
        _, file_name = os.path.split(input_file_path)
        #拡張子がmp4か
        if file_name[-4:] != '.mp4': return False
        #最大送信バイト数以下か
        if os.path.getsize(input_file_path) > pow(2, 32): return False

        return True


    def set_file_info(self, input_file_path: str) -> bool:
        is_set = self.file_validate(input_file_path)
        if not(is_set): is_set
        self.file_path = input_file_path
        self.file_size = os.path.getsize(input_file_path)
        return is_set
    

    def communication(self, tcp_client: TcpClient) -> None:
        tcp_client.socket.send(self.file_size.to_bytes(32, 'big'))
        with open(self.file_path, "rb") as f:
            while True:
                chunk = f.read(Config.MP4_MAX_STREAM_BYTES)
                if not chunk:
                    break
                tcp_client.socket.send(chunk)
        
        result_message = tcp_client.socket.recv(16).decode('utf-8')
        print(result_message)

def main():
    input_mp4_file_path    = input('input mp4 file path: ')
    mp4_file_upload_client = Mp4FileUploadClient()
    is_set = mp4_file_upload_client.set_file_info(input_mp4_file_path)
    if not(is_set):
        print('You have not selected the correct file.')
        exit()
    tcp_client = TcpClient()
    mp4_file_upload_client.communication(tcp_client)
    tcp_client.socket.close()

main()
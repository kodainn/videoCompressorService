import os

class Config:
    SERVER_ADDRESS          = 'localhost'
    SERVER_PORT             = 9001
    SERVER_FILE             = os.path.join(os.getcwd(), 'serverfile')

    CLIENT_ADDRESS          = 'localhost'
    CLIENT_PORT             = 0

    MP4_MAX_STREAM_BYTES    = 1400

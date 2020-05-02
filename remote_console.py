import socket
import struct

def pack_message(msg):
    msg = msg.encode('ASCII')
    packet = struct.pack("H{0}sx".format(len(msg)), len(msg) + 1, msg)
    return packet


def unpack_message(data):
    dataformat = "H{0}sx".format(struct.unpack("h", data[0:2])[0] - 1)
    data = struct.unpack(dataformat, data)
    return data


class RemoteConsoleClient():
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.connect()
        self.send('auth admin password')

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            print('connected to:', self.host, self.port)
        except socket.error as e:
            print(e)

    def send(self, msg):
        try:
            packet = pack_message(msg)
            self.client.send(packet)
            data = self.client.recv(4096)
            return unpack_message(data)[1].decode()

        except socket.error as e:
            print(e)

if __name__ == '__main__':
    REMOTE_CONSOLE_IP = '192.168.0.14'
    REMOTE_CONSOLE_PORT = 8991
    remoteconsole = RemoteConsoleClient(REMOTE_CONSOLE_IP, REMOTE_CONSOLE_PORT)

    useful_commands = ['getplayerlist', 'serverinput lalala', 'serverstatus', 'kick cid/name/playerid/profileid value', 'unbanall']
    server_input = remoteconsole.send('serverinput start')
    print('Response: ', server_input)
    server_input = remoteconsole.send('serverinput stop')
    print('Response: ', server_input)
    server_input = remoteconsole.send('serverinput start')
    print('Response: ', server_input)
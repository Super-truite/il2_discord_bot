import pandas as pd
from remote_console import RemoteConsoleClient
import urllib.parse
from tabulate import tabulate

server_params_dict = pd.read_csv('config.txt', sep=':', header=None, index_col=0, squeeze=True).to_dict()
REMOTE_CONSOLE_IP = server_params_dict['REMOTE_CONSOLE_IP']
REMOTE_CONSOLE_PORT = int(server_params_dict['REMOTE_CONSOLE_PORT'])
command_dict = pd.read_csv('command_for_remote_console.txt', header=None, index_col=0, squeeze=True, skiprows=1).to_dict()

# initializing the remote console
#remoteconsole = RemoteConsoleClient(REMOTE_CONSOLE_IP, REMOTE_CONSOLE_PORT)

ERROR_MESSAGES = {
    1: 'OK',
    2: 'unknown',
    3: 'unknown command',
    4: 'wrong parameter number',
    5: 'recieve buffer',
    6: 'incorrect authentification',
    7: 'server not running',
    8: 'server user',
    9: 'unknown user'
}


def to_df(s):
    s = urllib.parse.unquote(s)
    a = s.split('|')
    header = a[0].split(',')
    d = {k: [] for k in header}
    for row in a[2:]:
        row = row.split(',')
        for i, k in enumerate(d.keys()):
            d[k].append(row[i])

    return pd.DataFrame(d)


def to_ascii_table(s):
    df = to_df(s)
    df = df.drop(columns=['playerId', 'profileId'])
    return "```{}```".format(str(tabulate(df, tablefmt="pipe", headers="keys")))

def parse_response(s):
    S = urllib.parse.unquote(s)
    list_message = []
    element = []
    for s in S.split('&'):
        a = s.split('=')
        element.append(a[0])
        if '|' in a[1]:
            return to_ascii_table(a[1])
            element.append(to_ascii_table(a[1]))
        else:
            element.append(a[1])
        list_message.append(element)
    return list_message


def call_command(msg):
    '''
    call a remote client command
    :param msg: for instance "serverinput start" (string)
    :return: message to return to discord or error message (string)
    '''
    msg = msg[4:]
    print('command sent: ', msg)
    try:
        remoteconsole = RemoteConsoleClient(REMOTE_CONSOLE_IP, REMOTE_CONSOLE_PORT)
        response = remoteconsole.send(msg)
        print('server response: ', response)
        response = parse_response(response)
        if len(response) == 1:
            if response[0][1] == '1':
                return 'success'
            else:
                return ERROR_MESSAGES[int(response[0][1])]
        else:
            return response

    except Exception as e:
        print(e)
        return str(e)


def call_command_serverinput(msg):
    msg = msg.split(' ')[1]
    if msg in command_dict.keys():
        remoteconsole = RemoteConsoleClient(REMOTE_CONSOLE_IP, REMOTE_CONSOLE_PORT)
        auth = remoteconsole.send('auth admin password')
        print(auth)
        print('sending command: ', 'serverinput {}'.format(msg))
        server_input = remoteconsole.send('serverinput {}'.format(msg))
        print(server_input)
        print(command_dict[msg])
        return command_dict[msg]
    else:
        return 'invalid command'

if __name__ == '__main__':
    useful_commands = ['getplayerlist', 'serverinput lalala', 'serverstatus', 'kick name super-truite',
                       'unbanall']
    for c in useful_commands:
        call_command('$RC '+ c)
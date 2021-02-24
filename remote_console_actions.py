import pandas as pd
from remote_console import RemoteConsoleClient
import urllib.parse
from tabulate import tabulate
import time

server_params_dict = pd.read_csv('config.txt', sep=':', header=None, index_col=0, squeeze=True).to_dict()
REMOTE_CONSOLE_IP = server_params_dict['REMOTE_CONSOLE_IP']
REMOTE_CONSOLE_PORT = int(server_params_dict['REMOTE_CONSOLE_PORT'])
LOGIN_REMOTE_CONSOLE = server_params_dict['LOGIN_REMOTE_CONSOLE']
PASSWORD_REMOTE_CONSOLE = server_params_dict['PASSWORD_REMOTE_CONSOLE']


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
        # initializing the remote console
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
        return 'not passed'

def safe_call_command(msg):
    i = 0
    while i < 10:
        res = call_command(msg, verbose=False)
        if res != 'not passed':
            error = False
            return res
        time.sleep(1)
        i += 1
    raise Exception('Command did not execute after 10 trials')

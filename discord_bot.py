import discord
import sys
import pandas as pd
from remote_console_actions import call_command

DISCORD_BOT_TOKEN = sys.argv[1]

client = discord.Client()

server_params_dict = pd.read_csv('config.txt', sep=':', header=None, index_col=0, squeeze=True).to_dict()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$RC'):
        print(message.author)
        if str(message.author) in server_params_dict['Allowed_admin'].split(','):
            msg = call_command(message.content)
            await message.channel.send(str(msg))
        else:
            await message.channel.send('Cannot execute command. You are not an allowed admin')

client.run(DISCORD_BOT_TOKEN)



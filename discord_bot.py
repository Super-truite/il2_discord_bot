import discord
import sys
import os
from remote_console_actions import call_command, safe_call_command
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
client = discord.Client()
DISCORD_BOT_TOKEN = config['DEFAULT']['DISCORD_BOT_TOKEN']
ALLOWED_ADMINS = config['DEFAULT']['Allowed_admin']


client = discord.Client()


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

@client.event
async def on_message(message):
    if message.content.startswith('$RC'):
        if str(message.author) in ALLOWED_ADMINS.split(','):
            msg = safe_call_command(message.content)
            await message.channel.send(str(msg))
        else:
            await message.channel.send('You do not have the right to use the bot. Ask an admin')

client.run(DISCORD_BOT_TOKEN)



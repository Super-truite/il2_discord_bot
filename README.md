# Discord Bot to use the remote console in il2 ( python 3.7 )
this can be used to interact with Dserver from discord ( activate MCUs using
the serverinput command for instance)

## Remote console: Before installing, please make sure you know how to use and setup the il2 remote console.
Please follow the instructions p:173 of JimTM's guide (https://forum.il2sturmovik.com/topic/26303-il-2-sturmovik-mission-editor-and-multiplayer-server-manual/)
to setup your remote console. 
## Download 
download and extract anywhere on the machine were the il2 server is running:
https://github.com/Super-truite/il2_discord_bot/releases/download/v1/Il2DiscordBot.zip

## Bot Creation
* create a discord bot with send/read message permissions following those instructions: 
https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro
* copy the link provided in the OAuth2 page, copy paste it in your navigator and allow the bot on your discord server

## Configuration:
in the dist folder, modify the file config.ini:
* Change the IP and port in the config.ini (REMOTE_CONSOLE_IP, REMOTE_CONSOLE_PORT)
* You can allow users to talk to the console by adding them in the Allowed_admin line in config.ini. The format is a list of discord user names (fullname with # on their profile on discord) separated by ','
* You need to specify the login/password to the remote console in config.ini
* You need to add your discord bot token in config.ini . You can find your token on 
your application page in settings\bot : https://discordapp.com/developers/applications.
Do not share the token!

## Launch
click on discord_bot.exe inside the dist folder

## Usage
To send a serverinput command, say #RC 'command' in discord.
The bot should reply. For instance:
```
$RC kick name super-truite
$RC getplayerlist
$RC serverinput start
```
## For those wanting to modify the bot or if the executable do not work on your system:
## Python bot Installation
If you already have a working python installation, you can ignore 
the anaconda part and install in your environment the needed packages: discord.py, tabulate and pandas.
All this should be done on the machine where you run DServer.exe

* On your server, Install Anaconda: https://repo.anaconda.com/archive/Anaconda3-2019.10-Windows-x86_64.exe
* Launch Anaconda command prompt (windows key and type anaconda)
* cd to the discordBot folder and create the "il2" python  environment using this command:
```
conda env create -f environment.yml
```
* activate environment:
```
conda activate il2
```


## launch the discord bot:
```
python discord_bot.py 
```

```

## Thanks
Thanks to Coconut, Murleen and Sebj for helping me "talking" with the remote console :-)


 

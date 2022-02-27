import discord
from discord.ext import tasks
import os, time
from pirategame import Server, GameBoard, Member
from constants import Constants
from json import dumps, loads
from utils import log

global log_count, log_list
log_count, log_list = 0, []

if __name__ == "__main__":
    # Start the discord client
    client = discord.Client()

#* When client starts running:
@client.event
async def on_ready():
    # print response
    log('Logged in as {0.user}'.format(client))

    # start discord.ext.tasks loop
    update_server.start()

@tasks.loop(seconds=5.0)
async def update_server():
    # TODO check for people leaving/joining channels
    pass

            

@client.event
async def on_message(message):
    global game_server
    # message.author is who sent the message
    
    if message.author == client.user:
        return # Exit if the bot (client) sent the message
    
    #* If the channel is on a server:
    elif type(message.channel) == discord.channel.TextChannel:
        # * Command Parsing
        if message.content.startswith('!pirate') and message.channel.id == game_server.COMMAND_CHANNEL_ID:
            parts = message.content.split(' ')
            if parts[1].upper() == 'HELP':
                # Help command --> send a help message
                await message.channel.send(Constants.HELP_MESSAGE)

            elif parts[1].upper() == 'START':
                # create member list
                game_server.vcmembers = client.get_channel(game_server.VOICE_CHANNEL_ID).members
                # Start command --> Tell the server to start the game
                game_server.start_game()

            elif parts[1].upper() == 'TEST':
                #! Dev purposes only
                debug_var = None
                await message.channel.send(debug_var) 
        else:
            # Ignore this as not a valid command
            # TODO create an error message or just leave blank?
            pass

    #* If the channel is a DM to a user:
    elif type(message.channel) == discord.channel.DMChannel:
        response = game_server.message_recieved(message.author, message.content)
        if response:
            await message.author.send(response)

def main():
    global game_server

    # Init the game server
    game_server = Server(voice=938879048455712898, command=938902248946274364)
    #TODO need to make the bot get channel id for current vc
    #TODO need to be able to host multiple games at once

    # Start the discord client
    # TOKEN value is read from .env file
    client.run(TOKEN)
    
if __name__ == '__main__':
    TOKEN = None
    with open('.env') as file:
        for line in file.readlines():
            parts = line.split('=')
            exec('{}="{}"'.format(parts[0], parts[1]))
            # Reads value for TOKEN and saves to TOKEN

    main()


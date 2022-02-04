import discord
from discord.ext import tasks
import os, time
from pirategame import Server
from constants import Constants
from json import dumps, loads

global log_count, log_list
log_count, log_list = 0, []

def log(message: str, log_max: int = 5, print_to_console=True) -> None:
    global log_count, log_list

    log_list.append(message)
    if print_to_console:
        print(message)
    
    if log_count < log_max-1:
        log_count += 1
    else:
        log_count = 0
        with open('log.json', 'a') as file:
            file.append(dumps(
                {
                    'timestamp':time.time(),
                    'logs':log_list,
                },
                indent=4,))
        log_list = []
    return None

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
    #* Get the current game server
    global game_server

    #* Send data to the server for it to parse in .update()
    
    # Get the members currently in the voice chat and send to the server
    game_server.members = client.get_channel(game_server.VOICE_CHANNEL_ID).members
    #TODO check for people leaving/joining the vc
    
    #* call the update method on the server and parse all responses
    for response in game_server.update():
        # Format:
        # {
        #   'type':['message'],
        #   'subject:['all', member_id], # (who to send the message to)
        #   'content':'string containing the contents of the message'
        # }

        # ? Option to send messages to the server chat? Any reason this should be a feature?

        if response['type'] == 'message':
            if response['subject'] == 'all':
                for member in game_server.members:
                    # Print a message log
                    log(f'sending {member.id} {response["content"]}')
                    await member.send(response['content'])
            else:
                # send a message to a specific person
                pass

            

@client.event
async def on_message(message):
    global game_server
    # message.author is who sent the message
    
    if message.author == client.user:
        return # Exit if the bot (client) sent the message

    #* If the channel is a DM to a user:
    if type(message.channel) == discord.channel.DMChannel:
        response = game_server.message_recieved(message.author, message.content)
        if response:
            await message.author.send(response)
    
    #* If the channel is on a server:
    elif type(message.channel) == discord.channel.TextChannel:
        # * Command Parsing
        if message.content.startswith('!pirate') and message.channel.id == game_server.COMMAND_CHANNEL_ID:
            parts = message.content.split(' ')
            if parts[1].upper() == 'HELP':
                # Help command --> send a help message
                await message.channel.send(Constants.HELP_MESSAGE)

            elif parts[1].upper() == 'START':
                # Start command --> Tell the server to start the game
                game_server.start_game()
        else:
            # Ignore this as not a command
            pass

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


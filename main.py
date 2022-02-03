import discord
from discord.ext import tasks
import os
from pirategame import Server

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    update_server.start()

@tasks.loop(seconds=5.0)
async def update_server():
    global game_server
    
    game_server.members = client.get_channel(game_server.VOICE_CHANNEL_ID).members
    # TODO check for people leaving/joining the vc
    
    for response in game_server.update():
        if response['type'] == 'message':
            if response['subject'] == 'all':
                for member in game_server.members:
                    print(f'sending {member.id} {response["content"]}')
                    await member.send(response['content'])
            

@client.event
async def on_message(message):
    global game_server
    # message.author is who sent the message
    
    if message.author == client.user:
        return
    if type(message.channel) == discord.channel.DMChannel:
        response = game_server.message_recieved(message.author, message.content)
        if response:
            await message.author.send(response)
            
    elif type(message.channel) == discord.channel.TextChannel:
        # * Command Parsing
        if message.content.startswith('!pirate') and message.channel.id == game_server.COMMAND_CHANNEL_ID:
            parts = message.content.split(' ')
            if parts[1].upper() == 'START':
                game_server.start_game()

def main():
    global game_server
    game_server = Server(voice=938879048455712898, command=938902248946274364)
    client.run(TOKEN)
    
if __name__ == '__main__':
    with open('.env') as file:
        for line in file.readlines():
            parts = line.split('=')
            exec('{}="{}"'.format(parts[0], parts[1]))

    main()


import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('huzzah'):
        await message.channel.send('huzzah!')
with open('.env') as file:
    for line in file.readlines():
        parts = line.split('=')
        exec('{}="{}"'.format(parts[0], parts[1]))
print(TOKEN)
client.run(TOKEN)

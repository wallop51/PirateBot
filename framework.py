from abc import abstractmethod
import logging
import logging.config
import discord


from utils import EnvironmentContainer

class MemberManager:
    members = {}

    @classmethod
    def add_member(cls, discord_member: discord.Member):
        temp_member = cls.Member(discord_member)
        cls.members.update({discord_member.id:temp_member})
        del temp_member
    
    @classmethod
    def search_members(cls, id: int):
        try:
            return cls.members[id]
        except IndexError:
            print(f'No member with id of {id} found')
            return

    class Member:
        def __init__(self, discord_member: discord.Member):
            self.discord_member = discord_member
            self.name = discord_member.display_name
            self.id = discord_member.id


class Message:
    def __init__(self, content):
        self.content = content
        pass

class EmbedMessage(Message):
    def __init__(self, title, description, color, *fields):
        embed = discord.Embed(title=title, description=description, color=color)
        for field_data in fields:
            print(field_data)
            embed.add_field(**field_data)
        self.embed = embed


class BaseClass:
    def __init__(self, debug=True):
        logging_config_file = ('logging.conf' if not debug else 'logging_debug.conf')
        logging.config.fileConfig(
            fname=logging_config_file,
            disable_existing_loggers=False,
        )
        self.logger = logging.getLogger(__name__)

        self.logger.info('Logger has been initialised.')

        # setup environment variables
        self.environment = EnvironmentContainer()
        self.logger.info('Environment variables have been initialised.')

        self.client = discord.Client()
        self.logger.info('Discord client has been created.')

    def setup(self):
        @self.client.event
        async def on_ready():
            self.logger.info('Logged in as {0.user}'.format(self.client))
            print('Logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            self.message_recieved(message)

    def message_recieved(self, message):
        author = message.author

        if author == self.client.user:
            return # Exit as the client is recieving its own message

        channel = message.channel
        if type(channel) == discord.channel.TextChannel:
            self.recieved_group_channel(message)
        elif type(channel) == discord.channel.DMChannel:
            self.recieved_direct_message(message)
        else:
            print(f'Channels of type {type(channel)} are not yet supported.')

    @abstractmethod # Needs to be inplemented in next class up
    def recieved_group_channel(self, message):
        return
    @abstractmethod
    def recieved_direct_message(self, message):
        return
        
    
    def start_client(self):
        self.client.run(self.environment.TOKEN)

    async def send_direct_message(self, member: MemberManager.Member, message: Message, response_wanted: bool = False):
        try:
            if type(message) == Message:
                await member.discord_member.send(message.content)
            elif type(message) == EmbedMessage:
                await member.discord_member.send(embed=message.embed)
        except:
            print('An unknown error occurred')
    


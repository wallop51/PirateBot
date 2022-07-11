from exceptions import NotEnoughPlayers, NotInVC
import framework
from json import loads, dumps
from random import shuffle
from utils import LangContatiner, EnvironmentContainer
from discord import Message, Embed
import logging

# setup logger
global LOGGER
LOGGER = logging.getLogger(__name__)

# setup language container
global LANG
LANG = LangContatiner()
LOGGER.info(LANG.logger.info.logger.init.format(name=__name__))
LOGGER.info(LANG.logger.info.lang.init.format(name=__name__))

# setup environment variables
global ENV
ENV = EnvironmentContainer(required=("TOKEN",))
LOGGER.info(LANG.logger.info.env.init.format(name=__name__))

class Game:
    class Grid:
        @classmethod
        def random(cls):
            a = cls()
            a.randomise()
            return a
        weights = [1,1,1,1,1,1,1,1,1,1,1,1,2,10,25] # amount of each number
        def __init__(self, size=7):
            # stored as a 2 dimensional array of indexes 0-15
            self.items = [[None for i in range(size)] for j in range(size)]
        def __getitem__(self, coords): # access a particular square using a = Grid[x,y]
            x, y = coords
            return self.items[x][y]
        def __setitem__(self, coords, value): # write to a particular square using Grid[x,y] = a
            x, y = coords
            self.items[x][y] = value

        def randomise(self):
            # Generates a random grid for the player to use
            temp = [] # Add the correct proportions to a temporary list
            for i, weight in enumerate(self.weights):
                for j in range(weight): temp.append(i)
            shuffle(temp) # shuffle the list
            for i in range(len(self.items)): # split the list into a 2s array that can be used as the grid
                self.items[i] = temp[7*i:7*(i+1)]
            pass

        def __str__(self) -> str:
            # A function that returns the board as a string that can be sent to the player.
            lookup = loads("["+LANG.pirate.grid.order+"]")
            rows = ["" for i in range(len(self.items))]
            for i, row in enumerate(self.items):
                for item in row:
                    try:
                        rows[i] += LANG.pirate.grid.key.__getattr__(lookup[item])
                    except IndexError:
                        rows[i] += LANG.pirate.grid.key.none
            return eval('"'+LANG.pirate.grid.format.format(*rows)+'"')

    class Player:
        # An object that stores data regarding the players in the game
        def __init__(self, member):
            self.member = member
            self.id = member.id

            self.grid = None

            # Set default player settings
            self.cash_value = 0
            self.bank_value = 0
            # None  -> Not collected
            # True  -> Collected, not used
            # False -> Collected, used
            self.shield_status = None
            self.mirror_status = None

        def generate_grid(self):
            self.grid = Game.Grid.random()

        async def send(self, *args, **kwargs):
            return await self.member.send(*args, **kwargs)

    def __init__(self, players, master):
        # Setup variables
        self.active = True
        self.master = master

        # Create a way to store all of the player data
        self.players = {}
        self.player_ids = []
        for player in players:
            self.players.update({player.id: self.Player(player)})
            self.player_ids.append(player.id)

    async def send_grids(self):
        # distribute random grids
        for id, player in self.players.items():
            player.generate_grid()
            embed = Embed( title=LANG.pirate.message.embed.title,       description=LANG.pirate.message.embed.description)
            embed.add_field(name=LANG.pirate.message.embed.your_board,  value=str(player.grid), inline=True)
            embed.add_field(name=LANG.pirate.message.embed.players,     value=self.get_player_list(), inline=True)
            embed.add_field(name=LANG.pirate.message.embed.cash,        value=str(player.cash_value), inline=False)
            embed.add_field(name=LANG.pirate.message.embed.bank,        value=str(player.bank_value), inline=True)
            await player.send(embed=embed)

    def get_player_list(self):
        return '<@'+'>\n<@'.join(map(str, self.player_ids))+'>'


class App(framework.BaseClass):
    def __init__(self):
        super().__init__()

        self.voice_channel = None
        self.text_channel = None

    async def recieved_group_channel(self, message):
        pass
    async def recieved_command(self, message: Message):
        # parse the incoming commands and respond
        content = message.content
        parts = content.split(' ')
        
        # pirate help
        if parts[1].upper() == LANG.discord.command.help.upper():
            LOGGER.info(LANG.logger.command.help.format(user=message.author.display_name))
            await message.channel.send(LANG.pirate.message.help)

        # pirate dev ...
        elif parts[1].upper() == LANG.discord.command.dev.prefix.upper():
            #pirate dev generate_board
            if parts[2].upper() == LANG.discord.command.dev.generate_board.upper():
                LOGGER.info(LANG.logger.command.dev.generate_board.format(user=message.author.display_name))
                new_board = Game.Grid()
                new_board.randomise()
                await message.channel.send(str(new_board))

        # pirate start
        elif parts[1].upper() == LANG.discord.command.start.upper():
            if not message.author.voice:
                # If the user is not in a VC:
                a = NotInVC(message.channel)
                await a.send_message()
                # raise a

            self.voice_channel = message.author.voice.channel
            self.text_channel = message.channel

            # check that there are enough players to start the game
            debug = True
            if not (len(self.voice_channel.members) >= 2 or debug == True):
                a = NotEnoughPlayers(message.channel, len(self.voice_channel.members))
                await a.send_message()
                # raise a

            LOGGER.info(LANG.logger.info.game.start.format(author=message.author))

            await self.start_game(message.author)

    async def recieved_direct_message(self, message):
        pass

    async def start_game(self, master):
        self.current_game = Game(self.voice_channel.members, master)
        await self.text_channel.send(LANG.pirate.message.game_start.format(user_id=self.current_game.master.id))
        await self.current_game.send_grids()
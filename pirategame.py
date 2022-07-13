from exceptions import NotEnoughPlayers, NotInVC
import framework
from json import loads, dumps
from random import shuffle
from utils import LangContatiner, EnvironmentContainer
from discord import Message, Embed, Member
from random import choice
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
        def __init__(self, size: int=7):
            # stored as a 2 dimensional array of indexes 0-15
            self.items = [[None for i in range(size)] for j in range(size)]
        def __getitem__(self, coords: tuple) -> int: # access a particular square using a = Grid[x,y]
            x, y = coords
            return self.items[x][y]
        def __setitem__(self, coords: tuple, value: int): # write to a particular square using Grid[x,y] = a
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
                    except TypeError:
                        rows[i] += LANG.pirate.grid.key.none
            return eval('"'+LANG.pirate.grid.format.format(*rows)+'"')

    class Player:
        # An object that stores data regarding the players in the game
        def __init__(self, member: Member, pl: list):
            self.member = member
            self.id = member.id

            self.player_list = pl
            self.expect_response = False
            self.response_prompt = None
            self.is_ready1 = True
            self.is_ready2 = True

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
        
        def get_embed(self, desc: str='') -> Embed:
            # return the embed that the player will see after the tile has been selected
            embed = Embed( title=LANG.pirate.message.embed.title,       description=LANG.pirate.message.embed.description+desc)
            embed.add_field(name=LANG.pirate.message.embed.your_board,  value=str(self.grid), inline=True)
            embed.add_field(name=LANG.pirate.message.embed.players,     value=self.player_list, inline=True)
            embed.add_field(name=LANG.pirate.message.embed.cash,        value=str(self.cash_value), inline=False)
            embed.add_field(name=LANG.pirate.message.embed.bank,        value=str(self.bank_value), inline=True)
            return embed

        async def send(self, *args, **kwargs):
            # use player.send instead of player.member.send
            return await self.member.send(*args, **kwargs)
        
        async def send_square(self, square: str):
            self.is_ready1, self.is_ready2 = False, False
            x, y = int(square[1])-1, ord(square[0])-65
            square_type = self.grid[x,y]
            self.grid[x,y] = None
            description = self.handle_square(square_type)
            await self.send(embed=self.get_embed(LANG.pirate.message.square_chosen.format(square=square)+'\n'+description))

        def handle_square(self, square_type: int) -> Embed:
            # Select what happens when a square is chosen
            # "rob","kill","present","nuke","swap","choose","shield","mirror","bomb","double","bank","5K","3K","1K","200"
            self.expect_response = False
            if square_type == 0: # rob
                self.expect_response = True
            elif square_type == 1: # kill
                self.expect_response = True
            elif square_type == 2: # present
                self.expect_response = True
            elif square_type == 3: # nuke
                self.expect_response = True
            elif square_type == 4: # swap
                self.expect_response = True
            elif square_type == 5: # choose
                self.expect_response = True
            elif square_type == 6: # shield
                self.shield_status = True
            elif square_type == 7: # mirror
                self.mirror_status = True
            elif square_type == 8: # bomb
                self.cash_value = 0
            elif square_type == 9: # double
                self.cash_value *= 2
            elif square_type == 10: # bank
                self.bank_value = self.cash_value
                self.cash_value = 0
            elif square_type == 11: # 5K
                self.cash_value += 5000
            elif square_type == 12: # 3K
                self.cash_value += 3000
            elif square_type == 13: # 1K
                self.cash_value += 1000
            elif square_type == 14: # 200
                self.cash_value += 200

            if self.expect_response: self.response_prompt = square_type
            self.is_ready1 = not self.expect_response

            lookup = loads("["+LANG.pirate.grid.order+"]")
            description = LANG.pirate.grid.message.__getattr__(lookup[square_type])
            return description

    def __init__(self, players: list, master: Member):
        # Setup variables
        self.active = True
        self.master = master

        self.squares = [chr(65+i)+str(j+1) for i in range(7) for j in range(7)]

        # control logic
        self.player_choice_list = []

        # Create a way to store all of the player data
        self.player_ids = []
        for player in players:
            self.player_ids.append(player.id)
        self.players = {}
        pl = self.get_player_list()
        for player in players:
            self.players.update({player.id: self.Player(player, pl)})

        return

    async def send_grids(self):
        # distribute random grids
        for id, player in self.players.items():
            player.generate_grid()
            embed = player.get_embed()
            await player.send(embed=embed)

    def get_player_list(self):
        return '<@'+'>\n<@'.join(map(str, self.player_ids))+'>'

    async def round(self):
        # new round
        # Choose new tile
        # TODO Reset ready
        if len(self.player_choice_list) == 0:
            square = self.random_square()
        else:
            square = choice(self.player_choice_list)
            self.player_choice_list.remove(square)
        self.choose_square(square)

        # distribute the tile
        for player in self.players.values():
            await player.send_square(square)

    def random_square(self) -> str:
        return choice(self.squares)

    def choose_square(self, square: str):
        self.squares.remove(square)
        if square in self.player_choice_list:
            self.player_choice_list.remove(square)


class App(framework.BaseClass):
    def __init__(self):
        super().__init__()

        self.voice_channel = None
        self.text_channel = None

    async def recieved_group_channel(self, message: Message):
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

    async def start_game(self, master: Member):
        # starts the game
        self.current_game = Game(self.voice_channel.members, master)
        await self.text_channel.send(LANG.pirate.message.game_start.format(user_id=self.current_game.master.id))
        await self.current_game.send_grids()
        await self.current_game.round()